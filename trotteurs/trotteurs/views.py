from registration.backends.hmac.views import RegistrationView
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from django.views.generic import TemplateView

class RegistrationView(RegistrationView):
    """
        Registration view
    """
    template_name = 'registration/registration_form.html'

    def send_activation_email(self, user):
        """
            Send an email to confirm the address
        """
        super(RegistrationView, self).send_activation_email(user)

class ProfileView(LoginRequiredMixin, UpdateView):
    """
        Profile view
            User must be connected to access this page
    """
    template_name = 'trotteurs/profile.html'
    success_url = reverse_lazy('profile')
    models = Profile
    fields = '__all__'

    def get_object(self, queryset=None):
        """
            Return the profile
        """
        try:
            profile = self.request.user.profile
        except:
            return Profile.objects.model(user=self.request.user)
        return profile

class IndexView(TemplateView):
    """
        Index view
            view of the home
    """
    template_name = "trotteurs/home.html"


class AboutView(TemplateView):
    template_name = "trotteurs/about.html"


class ContactView(TemplateView):
    template_name = "trotteurs/contact.html"
