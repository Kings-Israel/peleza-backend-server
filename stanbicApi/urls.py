from django.contrib import admin
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    path("api/", include("main.urls")),
    path("api/auth/", include("authentication.urls")),
    path("__debug__/", include(debug_toolbar.urls)),
]
