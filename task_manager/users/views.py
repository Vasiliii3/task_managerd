from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from task_manager.users.models import CustomUser
from task_manager.users.forms import SignUpForm
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import CustomLoginRequiredMixin, \
    EditOwnAccountRequiredMixin, ProtectDeleteMixin


# Create your views here.
class UsersView(ListView):
    model = CustomUser
    template_name = 'users/users.html'
    context_object_name = 'users'
    ordering = ['id']
    extra_context = {
        'Description': _('Users'),
    }

    def get_queryset(self):
        """
        Exclude the administrator from the list
        """
        qs = super().get_queryset()
        return qs.exclude(is_superuser=True)


class CreateUserView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = SignUpForm
    template_name = 'forms.html'
    success_url = reverse_lazy('users_login')
    success_message = _("Registration successful")
    extra_context = {
        'Description': _('Create user'),
        'Button': _('Register'),
    }


class LoginUserView(SuccessMessageMixin, LoginView):
    template_name = 'forms.html'
    success_message = _('You are logged in!')
    extra_context = {
        'Description': _('Log In'),
        'Button': _('Enter'),
    }


class UserMixins(SuccessMessageMixin, CustomLoginRequiredMixin, EditOwnAccountRequiredMixin):
    message = _('You have no rights to change another user.')
    model = CustomUser
    success_url = reverse_lazy('users_home')


class UpdateUserView(UserMixins, UpdateView):
    form_class = SignUpForm
    template_name = 'forms.html'
    success_message = _("User is successfully updated")
    extra_context = {
        'Description': _('Update user'),
        'Button': _('Change'),
    }


class DeleteUserView(UserMixins, ProtectDeleteMixin, DeleteView):
    error_message = _("Unable to delete a user because he is being used")
    redirect_url = reverse_lazy('users_home')

    template_name = 'users/delete.html'
    success_message = _("User is successfully deleted")
    context_object_name = 'user'
    extra_context = {
        'Description': _('Delete user'),
    }
