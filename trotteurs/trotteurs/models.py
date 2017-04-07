from __future__ import unicode_literals
from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User

class Profile(models.Model):
    """
        An user profile is composed of :
            * an user
                - a username
                - [a first name]
                - [a last name]
                - an email
                - a password
            * [a country]

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = CountryField(blank=True)
