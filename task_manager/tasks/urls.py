from django.urls import path
from task_manager.tasks.views import TaskView, CreateTaskView, \
    UpdateTaskView, DeleteSTaskView, CurrentTaskView

urlpatterns = [
    path('', TaskView.as_view(), name='tasks_home'),
    path('create/', CreateTaskView.as_view(), name='tasks_creaate'),
    path('<int:pk>/update/', UpdateTaskView.as_view(), name='tasks_update'),
    path('<int:pk>/delete/', DeleteSTaskView.as_view(), name='tasks_delete'),
    path('<int:pk>/', CurrentTaskView.as_view(), name='tasks_current'),
]
