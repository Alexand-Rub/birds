from django.urls import path
from .views import (
    CreateObservationView,
    ListObservationView,
    DetailObservationView,
)


app_name = "observations"

urlpatterns = [
    path('', ListObservationView.as_view(), name='list'),
    path('create', CreateObservationView.as_view(), name='create'),
    path('<int:pk>', DetailObservationView.as_view(), name='detail'),
]