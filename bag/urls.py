""" url bag """
from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add/<course_id>/', views.add_to_bag, name='add_to_bag'),
    path('remove/<course_id>/', views.remove_course_from_bag,
         name='remove_course_from_bag'),
    ]
