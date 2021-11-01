from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class MainCategory(models.Model):

    main_category_name = models.CharField(max_length=254)
    main_category_friendly_name = models.CharField(max_length=254,
                                                   null=True, blank=True)

    def __str__(self):
        return self.main_category_name

    def get_friendly_name(self):
        return self.main_category_friendly_name


class Category(models.Model):
    category_name = models.CharField(max_length=254)
    category_friendly_name = models.CharField(max_length=254,
                                              null=True, blank=True)
    main_category = models.ForeignKey('MainCategory', null=True, blank=True,
                                      on_delete=models.SET_NULL)

    def __str__(self):
        return self.category_name

    def get_friendly_name(self):
        return self.category_friendly_name


class Courses(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=254)
    description = models.TextField()
    prerequisite = models.TextField()
    learning_objectives = models.TextField()
    for_whom = models.TextField()
    number_of_lectures = models.PositiveIntegerField()
    
    date_added = models.DateField(auto_now_add=True)
    time_added = models.TimeField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    time_updated = models.TimeField(auto_now=True)
    