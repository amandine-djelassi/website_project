from registration.backends.hmac.views import RegistrationView
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile

class RegistrationView(RegistrationView):
    template_name = 'registration/registration_form.html'

    def send_activation_email(self, user):
        super(RegistrationView, self).send_activation_email(user)

class ProfileView(LoginRequiredMixin, UpdateView):
    # form_class = forms.ProfileForm
    template_name = 'trotteurs/profile.html'
    success_url = reverse_lazy('profile')
    models = Profile
    fields = '__all__'

    def get_object(self, queryset=None):
        try:
            profile = self.request.user.profile
        except:
            return Profile.objects.model(user=self.request.user)
        return profile
