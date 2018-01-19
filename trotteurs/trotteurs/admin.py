from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django_countries.widgets import CountrySelectWidget
from .models import Newsletter, Checkpoint
from adminsortable2.admin import SortableAdminMixin
User = get_user_model()

class UserCreationForm(forms.ModelForm):
    """
        A form for creating new users.
        Includes all the required fields, plus a repeated password.
    """

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'country', 'is_active', 'is_admin')


    def clean_password2(self):
        """
            Check that the two password entries match
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """
            Save the provided password in hashed format
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
        A form for updating users.
        Includes all the fields on the user,
        but replaces the password field with admin's password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'country', 'username', 'is_active', 'is_admin', 'account_creation_date', 'last_visit_date')

    def clean_password(self):
        """
            Regardless of what the user provides, return the initial value.
            This is done here, rather than on the field, because the
            field does not have access to the initial value
        """
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    """
    """
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'first_name', 'last_name', 'country', 'is_admin', 'is_active', 'newsletter')
    list_filter = ('is_admin', 'country')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields':('first_name', 'last_name', 'country', 'newsletter', 'account_creation_date', 'last_visit_date')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'newsletter')}),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', 'account_creation_date', 'last_visit_date')
    ordering = ('-account_creation_date', 'email',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)


from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

class NewsletterAdmin(admin.ModelAdmin):
    change_form_template = 'admin/trotteurs/newsletter/change_form.html'
    list_display = ('subject', 'date', 'sent')
    model = Newsletter

    def render_change_form(self, request, context, *args, **kwargs):
        """
            We need to update the context to show the button.
        """
        context.update({'show_save_and_send': True})
        return super().render_change_form(request, context, *args, **kwargs)

    def response_post_save_change(self, request, obj):
        """
            This method is called by `self.changeform_view()` when the form
            was submitted successfully and should return an HttpResponse.
        """
        opts = self.model._meta
        pk_value = obj._get_pk_val()
        preserved_filters = self.get_preserved_filters(request)

        if '_save_and_send' in request.POST:

            users = User.objects.filter(newsletter=True)#.all()
            users_email = [user.email for user in users ]

            send_mail(obj.subject, obj.message, 'noreply@trotteurs.com', users_email)

            # print(product_item)
            obj.sent = True
            obj.save()
            post_url = reverse('admin:index', current_app=self.admin_site.name)
            return HttpResponseRedirect(post_url)

        else:
            # Otherwise, use default behavior
            return super().response_post_save_change(request, obj)

admin.site.register(Newsletter, NewsletterAdmin)

class CheckpointAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('city', 'date', 'reached', 'position')


admin.site.register(Checkpoint, CheckpointAdmin)
