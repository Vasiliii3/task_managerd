from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusForm
from task_manager.mixins import CustomLoginRequiredMixin, ProtectDeleteMixin
from django.utils.translation import gettext_lazy as _


class StatusMixins(SuccessMessageMixin, CustomLoginRequiredMixin, ):
    model = Status
    success_url = reverse_lazy('statuses_home')


class StatusView(StatusMixins, ListView):
    template_name = 'statuses/statuses.html'
    context_object_name = 'statuses'
    ordering = ['id']
    extra_context = {
        'Description': _('Statuses'),
    }


class CreateStatusView(StatusMixins, CreateView):
    form_class = StatusForm
    template_name = 'forms.html'
    success_message = _("Status successfully created")
    extra_context = {
        'Description': _('Create status'),
        'Button': _('Create'),
    }


class UpdateStatusView(StatusMixins, UpdateView):
    form_class = StatusForm
    template_name = 'forms.html'
    success_message = _("Status successfully changed")
    extra_context = {
        'Description': _('Change status'),
        'Button': _('Change'),
    }


class DeleteStatusView(StatusMixins, ProtectDeleteMixin, DeleteView):
    error_message = _("It is not possible to delete a status because it is in use")
    redirect_url = reverse_lazy('statuses_home')

    template_name = 'statuses/delete.html'
    success_message = _("Status successfully deleted")
    context_object_name = 'status'
    extra_context = {
        'Description': _('Delete status'),
    }
