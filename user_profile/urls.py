from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('profile/admin', views.admin_profile, name='admin'),
    path('add/course', views.add_course, name='add_course'),
    path('add/category', views.add_category, name='add_category'),
    path('add/main_category', views.add_main_category),
    path('add/main_category', views.add_main_category,
         name='add_main_category'),
    path('purchase_history', views.purchase_history,
         name='purchase_history'),
    path('purchase_history_details/<order_number>',
         views.purchase_history_details, name='purchase_history_details'),
    path('my_courses', views.my_courses, name='my_courses')
    ]
