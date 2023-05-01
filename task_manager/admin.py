from django.contrib import admin
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import CustomUser


# Register your models here.

@admin.register(Label, Status, CustomUser)
class MyTaskAdmin(admin.ModelAdmin):
    pass
