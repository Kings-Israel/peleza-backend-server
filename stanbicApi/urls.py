from django.contrib import admin
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    path("peleza-backend/api/", include("main.urls")),
    path("peleza-backend/api/auth/", include("authentication.urls")),
    path("peleza-backend/__debug__/", include(debug_toolbar.urls)),
]
