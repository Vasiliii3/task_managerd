from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class CustomLoginRequiredMixin(LoginRequiredMixin):
    message = _('You are not logged in! Please log in.')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.message)
            return redirect('users_login')
        return super().dispatch(request, *args, **kwargs)


class EditOwnAccountRequiredMixin:
    message = None

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if user.id == int(kwargs.get('pk')):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, self.message)
        return redirect(request.META.get('HTTP_REFERER'))


class ProtectDeleteMixin:
    error_message = None
    redirect_url = None

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.error_message)
            return redirect(self.redirect_url)