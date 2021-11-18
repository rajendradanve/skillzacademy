from django.contrib import admin
from .models import Course, Category, CourseSchedule, MainCategory
  
  
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


class CourseScheduleAdminInline(admin.TabularInline):
    model = CourseSchedule
    list_display = (
        'course_id',
        'course_date',
        'course_start_time',
        'course_end_time',
        'course_link',
    )
    
class CourseAdmin(admin.ModelAdmin):
    inlines = (CourseScheduleAdminInline,)
    list_display = (
        'title',
        'category',
        'created_by',
        'price',
        'rating',
        'image',
    )
  
  
admin.site.register(Course, CourseAdmin)
admin.site.register(Category, CategoryAdmin)
#admin.site.register(CourseSchedule, CourseScheduleAdmin)
admin.site.register(MainCategory, MainCategoryAdmin)
