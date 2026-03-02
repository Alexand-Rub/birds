from django.contrib import admin
from django.urls import path, include

from .views import (
    login_view,
    profile_view,
    ProfileView,
    logout_view,
    RegisterView,
    ProfileUpdateView
)

app_name = "userprofile"

urlpatterns = [
    path('', profile_view, name='profile'),
    path("<int:pk>/", ProfileView.as_view(), name='profile_pk'),
    path("<int:pk>/update", ProfileUpdateView.as_view(), name='update'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]