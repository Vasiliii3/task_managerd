from django.urls import path
from task_manager.users.views import CreateUserView, UsersView, \
    UpdateUserView, DeleteUserView

urlpatterns = [
    path('', UsersView.as_view(), name='users_home'),
    path('create/', CreateUserView.as_view(), name='users_create'),

    path('<int:pk>/update/', UpdateUserView.as_view(), name='users_update'),
    path('<int:pk>/delete/', DeleteUserView.as_view(), name='users_delete'),
]
