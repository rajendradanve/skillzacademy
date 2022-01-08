from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_courses, name='courses'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('add/course/', views.add_course, name='add_course'),
    path('add/category/', views.add_category, name='add_category'),
    path('select/category/', views.select_category, name='select_category'),
    path('update/category/<int:category_id>/', views.update_category,
         name='update_category'),
    path('add/main_category/', views.add_main_category,
         name='add_main_category'),
    path('update/main_category/<int:main_category_id>', views.update_main_category,
         name='update_main_category'),
    ]
