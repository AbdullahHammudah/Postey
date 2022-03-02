from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('posts', views.records, name='posts')
]