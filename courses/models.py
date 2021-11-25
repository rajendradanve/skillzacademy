from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class MainCategory(models.Model):

    class Meta: 
        verbose_name_plural = 'Main Categories'
        
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Category(models.Model):
    
    class Meta: 
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=False, blank=True)
    main_category = models.ForeignKey('MainCategory', null=False, blank=False,
                                      on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Course(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=254, null=False, blank=False)
    description = RichTextField()
    prerequisite = RichTextField()
    learning_objectives = RichTextField()
    for_whom = RichTextField()
    instructor_info = RichTextField()
    number_of_lectures = models.PositiveIntegerField()
    price = models.PositiveIntegerField(null=False, blank=False, default=100)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True,
                                 blank=True)

    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    date_added = models.DateField(auto_now_add=True)
    time_added = models.TimeField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    time_updated = models.TimeField(auto_now=True)

    def __str__(self):
        return self.title


class CourseSchedule(models.Model):
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE)
    course_date = models.DateField()
    course_start_time = models.TimeField()
    course_end_time = models.TimeField()
    course_link = models.URLField(max_length=1024, null=False, blank=False)
    course_timezone = models.CharField(max_length=100)
    date_added = models.DateField(auto_now_add=True)
    time_added = models.TimeField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    time_updated = models.TimeField(auto_now=True)
