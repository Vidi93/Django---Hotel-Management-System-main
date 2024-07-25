from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/assign-role/', views.assign_role, name='assign_role'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
]