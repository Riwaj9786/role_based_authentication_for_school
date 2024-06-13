from django.urls import path
from role_app import views

app_name = 'roles'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.registeruser, name='register'),
]