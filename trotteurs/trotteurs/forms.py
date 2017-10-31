from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from registration.forms import RegistrationForm
from django_countries.fields import LazyTypedChoiceField
from django_countries import countries
User = get_user_model()

class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class UserProfileRegistrationForm(RegistrationForm):
    username = forms.CharField(max_length=30, label='Username')
    country = forms.Select()
    first_name = forms.CharField(max_length=30, label='First name', required=False)
    last_name = forms.CharField(max_length=30, label='Last name', required=False)
    User = get_user_model()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'country', 'username')
