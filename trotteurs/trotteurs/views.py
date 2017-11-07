from registration.backends.hmac.views import RegistrationView
from django.views.generic.edit import UpdateView, FormView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from trotteurs.forms import UserProfileRegistrationForm, ContactForm

class RegistrationView(RegistrationView):
    """
        Registration view
    """
    template_name = 'registration/registration_form.html'
    form_class = UserProfileRegistrationForm

    def form_valid(self, form):
          # save the user
          response = super(RegistrationView, self).form_valid(form)
          # get the user creditials
          email = form.cleaned_data['email']
          password = form.cleaned_data['password1']
          # authenticate and login
        #   self.auth_login(self.request, email, password)

          return response

    def send_activation_email(self, user):
        """
            Send an email to confirm the address
        """
        super(RegistrationView, self).send_activation_email(user)

    def register(self, form):
        """
        Implement user-registration logic here.

        """
        User = get_user_model()
        user = User.objects.create_user(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password1'],
            first_name = form.cleaned_data['first_name'],
            username = form.cleaned_data['username'],
            last_name = form.cleaned_data['last_name'],
            country = form.cleaned_data['country']
        )
        self.send_activation_email(user)

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """
        Update Profile view
            User must be connected to access this page
    """
    User = get_user_model()
    model = User
    fields = ['first_name', 'last_name', 'country', 'avatar', 'about']
    template_name = 'trotteurs/profile_edit.html'
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

    # def form_valid(self, form):
    #     """
    #         This method is called when valid form data has been POSTed
    #         It should return an HttpResponse
    #     """
    #     form.send_email()
    #     return super(ContactView, self).form_valid(form)
