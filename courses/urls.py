from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_courses, name='courses'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('add/course/', views.add_course, name='add_course'),
    path('add/course_schedule/<int:course_id>/', views.add_course_schedule,
         name='add_course_schedule'),
    path('add/category/', views.add_category, name='add_category'),
    path('select/category/', views.select_category, name='select_category'),
    path('update/category/<int:category_id>/', views.update_category,
         name='update_category'),
    path('add/main_category/', views.add_main_category,
         name='add_main_category'),
    path('update/main_category/', views.update_main_category,
         name='update_main_category'),
    path('delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path('update/<int:course_id>/', views.update_course, name='update_course'),
    path('update/course_schedule/<int:course_id>/', views.update_course_schedule,
         name='update_course_schedule'),
    ]
