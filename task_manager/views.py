from django.contrib import messages
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _


class LogoutUserView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You logged out'))
        return super().dispatch(request, *args, **kwargs)


class LoginUserView(SuccessMessageMixin, LoginView):
    template_name = 'forms.html'
    success_message = _('You are logged in!')
    extra_context = {
        'Description': _('Log In'),
        'Button': _('Enter'),
    }
