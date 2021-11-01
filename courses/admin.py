from django.contrib import admin
from .models import Courses, Category, CourseSchedule, MainCategory

# Register your models here.
admin.site.register(Courses)
admin.site.register(Category)
admin.site.register(CourseSchedule)
admin.site.register(MainCategory)