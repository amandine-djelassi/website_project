from __future__ import unicode_literals
from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User


class Profile(models.Model):
    """
        An user profile is composed of :
            * an user
                - a username
                - an email
                - a password
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __init(self, *args, **kwargs):
        """
            Initialisation of the profile oject
        """
        super(Profile, self).__init__(*args, **kwargs)

    def __unicode__(self):
        """
            Name to use when "toString"
        """
        return self.user.username

    @property
    def email(self):
        """
            The email of the user
        """
        return self.user.email
