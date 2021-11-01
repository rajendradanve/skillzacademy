from django.contrib import admin
from .models import Course, Category, CourseSchedule, MainCategory

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'created_by',
        'price',
        'rating',
        'image',
    )
    

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
        'main_category',
    )


class MainCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class CourseScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'course_id',
        'course_date',
        'course_time',
        'course_link',
    )
    
    
admin.site.register(Course, CourseAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CourseSchedule, CourseScheduleAdmin)
admin.site.register(MainCategory, MainCategoryAdmin)
