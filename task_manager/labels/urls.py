from django.urls import path
from task_manager.labels.views import LabelsView, CreateLabelsView, \
    UpdateLabelsView, DeleteLabelsView

urlpatterns = [
    path('', LabelsView.as_view(), name='lablels_home'),
    path('create/', CreateLabelsView.as_view(), name='lablels_creaate'),
    path('<int:pk>/update/', UpdateLabelsView.as_view(), name='lablels_update'),
    path('<int:pk>/delete/', DeleteLabelsView.as_view(), name='lablels_delete'),
]
