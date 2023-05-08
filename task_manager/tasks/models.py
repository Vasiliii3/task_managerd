from django.db import models
from task_manager.users.models import CustomUser
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, verbose_name=_('Status'), related_name='status')
    author = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name='author')
    executor = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, null=True, blank=True, verbose_name=_('Executor'),
        related_name='executor')
    labels = models.ManyToManyField(
        Label, through='TaskLabels', through_fields=('task', 'label'), blank=True,
        verbose_name=_('Labels'), related_name='labels')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TaskLabels(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
