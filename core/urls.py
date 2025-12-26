from django.urls import path
from .views import UserList, TaskList, TaskDetail

urlpatterns = [
    path('users/', UserList.as_view()),
    path('tasks/', TaskList.as_view()),
    path('tasks/<str:pk>/', TaskDetail.as_view()),
]
