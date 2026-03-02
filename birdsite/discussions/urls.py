from django.contrib import admin
from django.urls import path, include
from .views import (
    CreateDiscussionView,
    ListDiscussionView,
    MyListDiscussionView,
    DetailDiscussionView,
    DeleteDiscussionView,
    DeleteMessageView,
)

app_name = "discussions"

urlpatterns = [
    path('', ListDiscussionView.as_view(), name='list'),
    path('my', MyListDiscussionView.as_view(), name='my_list'),
    path('create', CreateDiscussionView.as_view(), name='create'),
    path('<int:pk>', DetailDiscussionView.as_view(), name='detail'),
    path('<int:pk>/discussions_delete', DeleteDiscussionView.as_view(), name='delete_discussion'),
    path('<int:pk>/massage_delete', DeleteMessageView.as_view(), name='delete_massage'),
]