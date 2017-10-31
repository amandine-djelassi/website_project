from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django_countries.fields import CountryField
from django.core.files.storage import FileSystemStorage
from django.db.models.fields.files import ImageFieldFile
from django.utils.functional import cached_property
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.template.defaultfilters import slugify
class OverwriteStorage(FileSystemStorage):
    """
        When saving an image, this storage class deletes existing file,
        thus implementing the overwriting feature
    """
    def get_available_name(self, name):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


def avatar_name_path(instance, filename):
    """
        Convert arbitrary file name to the string consisting
        of email_name and user ID
    """
    extension = filename[filename.rfind('.'):]
    new_path = 'user_profile/%s%s%s' % (instance.user.get_email_name(), instance.user.pk, extension)
    return new_path


class MyImageFieldFile(ImageFieldFile):
    """
        Return default avatar if there is no image
    """
    @property
    def url(self):
        try:
            result = super(MyImageFieldFile, self)._get_url()
            if not os.path.isfile(self.path):
                raise ValueError
        except ValueError:
            result = settings.DEFAULT_AVATAR_URL if hasattr(settings, 'DEFAULT_AVATAR_URL') else ''
        return result


class MyImageField(models.ImageField):
    attr_class = MyImageFieldFile


class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, is_admin=False, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        email=self.normalize_email(email)
        user = self.model(email=email,
                        is_admin=is_admin,
                        slug=slugify(username),
                        **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, username, password=None, **extra_fields):
        """
            Create regular user
        """
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        """
            Create super user
        """
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(email, username, password, is_admin=True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
        A user is composed of :
            email
            first_name
            last_name
            country
            *is_active
            *is_admin
    """
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    first_name = models.CharField(
        verbose_name='first name',
        max_length=30,
        blank=True,
        help_text=('Required. 30 characters or fewer. Letters, digits and ''@/./+/-/_ only.'),
        validators=[RegexValidator(r'^[\w.+-]+$', ('Enter a valid first name.'), 'invalid')]
    )

    last_name = models.CharField(
        verbose_name='last name',
        max_length=30,
        blank=True,
        help_text=('Required. 30 characters or fewer. Letters, digits and ''@/./+/-/_ only.'),
        validators=[RegexValidator(r'^[\w.+-]+$', ('Enter a valid last name.'), 'invalid')]
    )
    # country of residence. 3rd party component,
    # saved as ISO code, displayed as full name.
    # Input control is a dropdown list, supporting localisation
    country = CountryField(blank_label='(select country)', blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # username present only to avoid error
    username = models.CharField('username', max_length=30, null=True, blank=True, unique=True)

    avatar = MyImageField(storage=OverwriteStorage(), upload_to=avatar_name_path, blank=True)
    # "about me", biography text field
    about = models.TextField(max_length=500, blank=True)
    slug = models.SlugField(max_length=30, unique=True)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # def __init__(self, *args, **kwargs):
    #     # __original_avatar is used to detect avatar change, to run avatar resize procedure only when needed
    # __original_avatar = avatar

    def __str__(self):
        return self.email

    def resize_avatar(self):
        # code from with some changes : http://www.yilmazhuseyin.com/blog/dev/create-thumbnails-imagefield-django/
        if not self.avatar:
            return

        AVATAR_SIZE = settings.AVATAR_SIZE
        image = Image.open(BytesIO(self.avatar.read()))
        if self.avatar.name.lower().endswith('png'):
            bg = Image.new("RGB", image.size, (255, 255, 255))
            bg.paste(image, image)
        else:
            bg = image
        min_dimension = min(image.size[0], image.size[1])
        image = ImageOps.fit(bg, (min_dimension, min_dimension))
        image = image.resize(AVATAR_SIZE, Image.ANTIALIAS)

        temp_handle = BytesIO()
        image.save(temp_handle, 'jpeg')
        temp_handle.seek(0)

        suf = SimpleUploadedFile(os.path.split(self.avatar.name)[-1], temp_handle.read(), content_type='image/jpeg')
        self.avatar.save('%s.%s' % (os.path.splitext(suf.name)[0], 'jpg'), suf, save=False)

    def save(self, *args, **kwargs):
        # if self.avatar != self.__original_avatar:
        self.resize_avatar()
        super(User, self).save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
            Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_email_name(self):
        """
            Return the part before @ of the email
        """
        name = self.email.split('@',1)[0]

    def get_short_name(self):
        """
            return the first name of the user is field
            the email name sonst
        """
        if self.first_name != "" :
            name = self.first_name
        else:
            name = self.get_email_name()

        return name
