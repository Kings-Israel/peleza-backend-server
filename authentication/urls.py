from django.urls import path
from rest_framework import views
from .views import Login, Profile

urlpatterns = [
    path("login/", Login.as_view()),
    path("profile/", Profile.as_view()),
]
