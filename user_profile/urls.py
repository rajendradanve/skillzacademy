from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('profile', views.admin_profile, name='admin'),
    path('add/course', views.add_course, name='add_course'),
    ]
