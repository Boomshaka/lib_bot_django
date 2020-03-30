from django.contrib import admin
from django.urls import path

from .views import (
    ErrorStatDetailView,
    ErrorStatListView
)

app_name = 'stat'

urlpatterns = [
    path('<int:id>/', ErrorStatDetailView.as_view(), name = 'stat-detail'),
    path('', ErrorStatListView.as_view(), name = 'stat-list')
]