
from django.contrib import admin
from django.urls import path

from .views import (
    home_view,
    run_script,
)

app_name = 'main'
urlpatterns = [
    path('', home_view, name='home'),
    path('run/', run_script, name='script'),
]
