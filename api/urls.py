from django import views
from django.urls import path
from .views import posts
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('posts/records', posts.as_view({'get':'records'})),
    path('posts/create', posts.as_view({'post':'create'})),
    path('posts/<str:id>', posts.as_view({'get':'record'})),
    path('posts/<str:id>/update', posts.as_view({'put':'update'})),
    path('posts/<str:id>/delete', posts.as_view({'delete':'delete'})),
    path('login', obtain_auth_token, name='login'),
]