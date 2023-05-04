from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.labels.models import Label
from task_manager.labels.forms import LabelForm
from task_manager.mixins import CustomLoginRequiredMixin, RelatedObjectDeleteMixin
from django.utils.translation import gettext_lazy as _

# Create your views here.


class LabelMixins(SuccessMessageMixin, CustomLoginRequiredMixin, ):
    model = Label
    success_url = reverse_lazy('lablels_home')


class LabelsView(LabelMixins, ListView):
    template_name = 'labels/labels.html'
    context_object_name = 'labels'
    ordering = ['id']
    extra_context = {
        'Description': _('Labels'),
    }


class CreateLabelsView(LabelMixins, CreateView):
    form_class = LabelForm
    template_name = 'forms.html'
    success_message = _("Label successfully created")
    extra_context = {
        'Description': _('Create label'),
        'Button': _('Create'),
    }


class UpdateLabelsView(LabelMixins, UpdateView):
    form_class = LabelForm
    template_name = 'forms.html'
    success_message = _("Label successfully changed")
    extra_context = {
        'Description': _('Change label'),
        'Button': _('Change'),
    }


class DeleteLabelsView(LabelMixins, RelatedObjectDeleteMixin, DeleteView):
    message = _("It is not possible to delete a label because it is in use")
    redirection = reverse_lazy('lablels_home')

    template_name = 'labels/delete.html'
    success_message = _("Label successfully deleted")
    context_object_name = 'label'
    extra_context = {
        'Description': _('Delete label'),
    }
