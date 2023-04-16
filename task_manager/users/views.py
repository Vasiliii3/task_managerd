from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import CustomUser
from .forms import SignUpForm
from django.utils.translation import gettext_lazy as _


# Create your views here.


class CreateUserView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = SignUpForm
    template_name = 'forms.html'
    success_url = reverse_lazy('login')
    extra_context = {
        'Description': _('Create user'),
        'Button': _('Register'),
    }
    success_message = _("Registration successful")


class LoginUserView(SuccessMessageMixin, LoginView):
    template_name = 'forms.html'
    extra_context = {
        'Description': _('Log In'),
        'Button': _('Sign in'),
    }
    success_message = _('You are logged in!')

