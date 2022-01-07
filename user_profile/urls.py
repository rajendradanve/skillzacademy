from django.urls import path
from . import views

urlpatterns = [
    path('profile/admin/', views.admin_profile, name='admin'),
    path('purchase_history/', views.purchase_history,
         name='purchase_history'),
    path('purchase_history_details/<order_number>/',
         views.purchase_history_details, name='purchase_history_details'),
    path('my_courses/', views.my_courses, name='my_courses')
    ]
