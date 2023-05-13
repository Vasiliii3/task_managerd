from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django_filters.views import FilterView
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm
from task_manager.mixins import CustomLoginRequiredMixin, EditOwnObjeRequiredMixin
from django.utils.translation import gettext_lazy as _
from task_manager.tasks.filters import TaskFilter


class TaskMixins(SuccessMessageMixin, CustomLoginRequiredMixin, ):
    model = Task
    success_url = reverse_lazy('tasks_home')


class TaskView(TaskMixins, FilterView):
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'
    ordering = ['id']
    filterset_class = TaskFilter
    extra_context = {
        'Description': _('Tasks'),
    }


class CurrentTaskView(TaskMixins, DetailView):
    template_name = 'tasks/current.html'
    context_object_name = 'task'
    extra_context = {
        'Description': _('Task preview'),
    }


class CreateTaskView(TaskMixins, CreateView):
    form_class = TaskForm
    template_name = 'forms.html'
    success_message = _("Task successfully created")
    extra_context = {
        'Description': _('Create task'),
        'Button': _('Create'),
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTaskView(TaskMixins, UpdateView):
    form_class = TaskForm
    template_name = 'forms.html'
    success_message = _("Task successfully changed")
    extra_context = {
        'Description': _('Task change'),
        'Button': _('Change'),
    }


class DeleteSTaskView(TaskMixins, EditOwnObjeRequiredMixin, DeleteView):
    message = _('A task can only be deleted by its author')

    template_name = 'tasks/delete.html'
    success_message = _("Task successfully deleted")
    context_object_name = 'task'
    extra_context = {
        'Description': _('Delete task'),
    }
