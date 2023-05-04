from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
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
        if user.is_authenticated and user.id == int(kwargs.get('pk')):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, self.message)
        return redirect(request.META.get('HTTP_REFERER'))


class RelatedObjectDeleteMixin:
    message = None
    redirection = None

    def delete(self, *args, **kwargs):
        try:
            super().delete(*args, **kwargs)
        except models.ProtectedError:
            message = self.message
            return HttpResponseRedirect(reverse(self.redirection) + f'?error={message}')
