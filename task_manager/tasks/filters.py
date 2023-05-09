import django_filters
from django import forms

from task_manager.tasks.models import Task
from django.utils.translation import gettext_lazy as _


class TaskFilter(django_filters.FilterSet):
    is_author = django_filters.BooleanFilter(
        field_name='author', label=_('Show only my records'),
        method='filter_is_author', widget=forms.CheckboxInput,
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'is_author']

    def filter_is_author(self, queryset, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
