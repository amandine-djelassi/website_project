from registration.backends.hmac.views import RegistrationView
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationView(RegistrationView):
    """
        Registration view
    """
    template_name = 'registration/registration_form.html'

    def form_valid(self, form):
        # save the user
        response = super(RegistrationView, self).form_valid(form)
        # get the user creditials
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        # authenticate and login
        self.auth_login(self.request, email, password)

        return response



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
    # User = get_user_model()
    models = User
    fields = '__all__'

    def get_object(self, queryset=None):
        """
            Return the profile
        """
        # User = get_user_model()
        try:
            profile = self.request.user.profile
        except:
            return User.objects.model(user=self.request.user)
        return profile

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


class ContactView(TemplateView):
    """
        The contact view
    """
    template_name = "trotteurs/contact.html"
