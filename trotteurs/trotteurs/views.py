from registration.backends.hmac.views import RegistrationView, ActivationView
from django.views.generic.edit import UpdateView, FormView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
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
    # template_name = 'registration/registration_form.html'
    # form_list=[RegistrationForm1, RegistrationForm2]
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
                self.country = "ok" #form.cleaned_data['country']
                self.newsletter = form.cleaned_data['Newsletter']

        user = self.save_user()

        self.send_activation_email(user)
        return HttpResponseRedirect('/accounts/register/complete/')


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """
        Update Profile view
            User must be connected to access this page
    """
    User = get_user_model()
    model = User
    fields = ['first_name', 'last_name', 'country', 'avatar', 'about']
    template_name = 'registration/profile_edit.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def user_passes_test(self, request):
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect_to_login(request.get_full_path())
        return super(UpdateProfileView, self).dispatch(
            request, *args, **kwargs)


class IndexView(TemplateView):
    """
        Index view
            view of the home
    """
    template_name = "trotteurs/home.html"

class AboutView(TemplateView):
    """
        The about view
    """
    template_name = "trotteurs/about.html"


class ContactView(FormView):
    """
        The contact view
    """
    template_name = "trotteurs/contact.html"
    form_class = ContactForm
    success_url = '/'
