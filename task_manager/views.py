from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.utils.translation import gettext_lazy as _


class LogoutUserView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You logged out'))
        return super().dispatch(request, *args, **kwargs)
