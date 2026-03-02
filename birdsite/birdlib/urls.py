from django.contrib import admin
from django.urls import path, include

from .views import (
    CreateBirdView,
    ListBirdView,
    FavouritesListBirdView,
    DetailBirdView,
    DeleteBirdView,
)

app_name = "birdlib"

urlpatterns = [
    path('', ListBirdView.as_view(), name='list'),
    path('favourites', FavouritesListBirdView.as_view(), name='favourites'),
    path('create/', CreateBirdView.as_view(), name='create'),
    path('bird/<int:pk>', DetailBirdView.as_view(), name='details'),
    path('bird/<int:pk>/bird_delete', DeleteBirdView.as_view(), name='delete'),
]