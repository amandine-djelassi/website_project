from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django_countries.fields import CountryField
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
import datetime
from ckeditor_uploader.fields import RichTextUploadingField

class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, is_admin=False, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        email=self.normalize_email(email)
        user = self.model(username=username,
                        email=email,
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
            username
            email
            first_name
            last_name
            country
            newsletter
            account_creation_date
            last_visit_date
            is_active
            is_admin
    """
    username = models.CharField(
        verbose_name=_('Username'),
        max_length=30,
        unique=True,
        error_messages={'unique': _("This username already exists.")}
    )

    email = models.EmailField(
        verbose_name=_('Email address'),
        max_length=255,
        unique=True,
        error_messages={'unique': _("This email has already been registered.")}
    )

    first_name = models.CharField(
        verbose_name=_('First name'),
        max_length=30,
        blank=True,
        validators=[RegexValidator(r'^[\w.+-]+$', _('Enter a valid first name.'), 'invalid')]
    )

    last_name = models.CharField(
        verbose_name=_('Last name'),
        max_length=30,
        blank=True,
        validators=[RegexValidator(r'^[\w.+-]+$', _('Enter a valid last name.'), 'invalid')]
    )

    country = CountryField(
        verbose_name=_('Country'),
        blank=True
    )

    newsletter = models.BooleanField(
        verbose_name=_('Newsletter'),
        default=False,
        blank=True
    )

    account_creation_date = models.DateField(
        verbose_name=_('Account creation date'),
        default=datetime.date.today,
    )

    last_visit_date = models.DateField(
        verbose_name=_('Last visit date'),
        default=datetime.date.today,
    )

    is_active = models.BooleanField(verbose_name=_('Active'), default=True)
    is_admin = models.BooleanField(verbose_name=_('Admin'), default=False)

    slug = models.SlugField(max_length=30, unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """
            Does the user have a specific permission?
        """
        return True

    def has_module_perms(self, app_label):
        """
            Does the user have permissions to view the app `app_label`?
        """
        return True

    @property
    def is_staff(self):
        """
            Is the user a member of staff?
        """
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

class Newsletter(models.Model):
    """
        A newsletter is composed of :
            subject
            message
            date
            sent boolean if the email is send or not
    """

    class Meta:
        verbose_name = _('Newsletter')
        verbose_name_plural = _('Newsletters')

    subject = models.CharField(
        verbose_name=_('Subject'),
        max_length=200
    )

    date = models.DateField(
        verbose_name=_('Publication date'),
        default=datetime.date.today
    )

    message = RichTextUploadingField(
        verbose_name=_('Message')
    )

    sent = models.BooleanField(
        verbose_name=_('Sent'),
        default=False
    )

class Checkpoint(models.Model):
    """
        A checkpoint is composed of :

    """

    class Meta:
        verbose_name = _('Checkpoint')
        verbose_name_plural = _('Checkpoints')
        ordering = ['position']

    name = models.CharField(
        verbose_name=_('Name'),
        max_length=200,
        unique=True
    )

    date = models.DateField(
        verbose_name=_('Date'),
        blank=True,
        null=True
    )

    latitude = models.DecimalField(
        verbose_name=_('Latitude'),
        decimal_places=10,
        max_digits=15
    )

    longitude = models.DecimalField(
        verbose_name=_('Longitude'),
        decimal_places=10,
        max_digits=15
    )

    reached = models.BooleanField(
        verbose_name=_('City reached'),
        default=False,
    )

    position = models.PositiveIntegerField(default=0, blank=False, null=False)
