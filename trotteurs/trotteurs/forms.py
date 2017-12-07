from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from registration.forms import RegistrationForm
from django.utils.translation import ugettext_lazy as _
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

class RegistrationForm1(RegistrationForm):

    username = forms.CharField(
        max_length=30,
        label=_('Username'),
        widget=forms.TextInput(attrs={'placeholder': _('username')})
    )

    email = forms.EmailField(
        label=_('Email address'),
        widget=forms.TextInput(attrs={'placeholder': _('email address')})
    )

    User = get_user_model()

    class Meta:
        model = User
        fields = ('username', 'email')

class RegistrationForm2(forms.Form):

    first_name = forms.CharField(
        max_length=30,
        label=_('First name'),
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('first name')})
    )

    last_name = forms.CharField(
        max_length=30,
        label=_('Last name'),
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('last name')})
    )

    #country = forms.Select()
    country = LazyTypedChoiceField(choices=countries)

    newsletter = forms.BooleanField(
        label=_("Register to the newsletter"),
        required=False
    )

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(
        required=True,
        widget=forms.Textarea
    )
