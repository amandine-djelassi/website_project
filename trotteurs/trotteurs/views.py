from registration.backends.hmac.views import RegistrationView, ActivationView
from django.views.generic.edit import UpdateView, FormView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from trotteurs.forms import ContactForm, RegistrationForm1, RegistrationForm2

from django.shortcuts import render_to_response
from formtools.wizard.views import SessionWizardView
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.utils.encoding import force_text
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from trotteurs.models import Checkpoint

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/activate.html', {'active': True,})
    else:
        return render(request, 'registration/activate.html', {'active': False,})

FORMS = [("user", RegistrationForm1),
("profile", RegistrationForm2)]

TEMPLATES = {"0": 'registration/registration_form1.html',
"1": 'registration/registration_form2.html'}
class RegistrationView(SessionWizardView):
    def get_template_names(self):
            return [TEMPLATES[self.steps.current]]

    def send_activation_email(self, user):
        """
            Send an email to confirm the address
        """
        subject = 'Activate Your MySite Account'
        message = render_to_string('registration/account_activation_email.html', {
            'user': user,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })

        email = EmailMessage(subject, message, to=[self.email])
        email.send()


    def save_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            username=self.username,
            last_name=self.last_name,
            country=self.country,
            newsletter=self.newsletter,
            is_active=False
        )
        return user

    def done(self, form_list, **kwargs):
        for form in form_list:
            if isinstance(form, RegistrationForm1):
                self.email = form.cleaned_data['email']
                self.password=form.cleaned_data['password1']
                self.username = form.cleaned_data['username']
            else:
                self.first_name = form.cleaned_data['first_name']
                self.last_name = form.cleaned_data['last_name']
                self.country = form.cleaned_data['country']
                self.newsletter = form.cleaned_data['newsletter']

        user = self.save_user()

        self.send_activation_email(user)
        return HttpResponseRedirect('/accounts/register/complete/')

from django.urls import reverse

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """
        Update Profile view
            User must be connected to access this page
    """
    template_name = 'registration/profile_edit.html'
    User = get_user_model()
    model= User
    fields=["first_name", "last_name", "newsletter", "username", "country"]
    success_url = '/'


    def dispatch(self, request, slug, *args, **kwargs):
        if not (request.user.slug == slug):
            return redirect('profile_edit', slug=request.user.slug)
        return super(UpdateProfileView, self).dispatch(
            request, *args, **kwargs)

class IndexView(TemplateView):
    """
        Index view
            view of the home
    """
    template_name = "trotteurs/home.html"

class RouteView(LoginRequiredMixin, ListView):
    """
        Create a view with all the countries in the db
    """
    template_name = 'trotteurs/route.html'
    context_object_name = 'checkpoint_list'


    def get_queryset(self):
        """
            Return all the checkpoint
        """
        return Checkpoint.objects.order_by('position')[:]


def contact(request):
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
            message = request.POST.get('message', '')
            subject = request.POST.get('subject', '')

            # Email the profile with the contact information
            template = get_template('trotteurs/contact_template.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'message': message,
                'subject': subject,
            }
            content = template.render(context)

            email = EmailMessage(
                '[Contact] ' + subject,
                content,
                "Trotteurs.fr",
                ['amandine.djelassi@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return redirect('contact')
    return render(request, 'trotteurs/contact.html', {
        'form': form_class,
    })

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })

class confirm_delete_account(TemplateView):
    """
    """
    template_name = "registration/confirm_delete_account.html"

def delete_account(request):
    request.user.delete()
    logout(request)
    return render(request, 'trotteurs/home.html')
