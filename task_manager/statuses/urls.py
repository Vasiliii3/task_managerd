from django.urls import path
from task_manager.statuses.views import StatusView, CreateStatusView, \
    UpdateStatusView, DeleteStatusView

urlpatterns = [
    path('', StatusView.as_view(), name='statuses_home'),
    path('create/', CreateStatusView.as_view(), name='statuses_create'),
    path('<int:pk>/update/', UpdateStatusView.as_view(), name='statuses_update'),
    path('<int:pk>/delete/', DeleteStatusView.as_view(), name='statuses_delete'),
]
