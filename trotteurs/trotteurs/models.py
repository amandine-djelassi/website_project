from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin

class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_admin=False, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        email=self.normalize_email(email)
        user = self.model(email=email,
                        is_admin=is_admin,
                        **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        """
            Create regular user
        """
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
            Create super user
        """
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(email, password, is_admin=True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
        A user is composed of :
            email
            first_name
            last_name
            is_active
            is_admin
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

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # username present only to avoid error
    username = models.CharField('username', max_length=30, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

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

    def get_short_name(self):
        """
            return the first name of the user is field
            the email name sonst
        """
        if self.first_name != "":
            name = self.first_name
        else:
            name = self.email.split('@',1)[0]
        return name
