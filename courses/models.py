from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.timezone import now


class MainCategory(models.Model):

    class Meta: 
        verbose_name_plural = 'Main Categories'
        
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name
    
    def _generate_name(self):
        """
        generate name from the friendly name removing spaces and using lowercase
        """
        return self.friendly_name.lower().replace(' ', '_')
    
    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.name:
            self.name = self._generate_name()
        super().save(*args, **kwargs)


class Category(models.Model):
    
    class Meta: 
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=False, blank=True)
    main_category = models.ForeignKey('MainCategory', null=False, blank=False,
                                      on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def _generate_name(self):
        """
        generate name from the friendly name removing spaces and using lowercase
        """
        return self.friendly_name.lower().replace(' ', '_')

    def get_friendly_name(self):
        return self.friendly_name
    
    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.name:
            self.name = self._generate_name()
        super().save(*args, **kwargs)


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
    start_date = models.DateField(default=now)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True,
                                 blank=True)

    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    date_added = models.DateField(auto_now_add=True)
    time_added = models.TimeField(auto_now_add=True)
    date_updated = models.DateField()
    time_updated = models.TimeField()
    course_timezone = models.CharField(max_length=100, default="CET")

    def update_start_date(self):
        
        self.start_date = self.courseschedulelist.order_by('course_date').first().course_date
        self.save()

    def __str__(self):
        return self.title


class CourseSchedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                                  related_name='courseschedulelist')
    course_date = models.DateField()
    course_start_time = models.TimeField()
    course_end_time = models.TimeField()
    course_link = models.URLField(max_length=1024, null=False, blank=False)
    date_added = models.DateField(auto_now_add=True)
    time_added = models.TimeField(auto_now_add=True)
    date_updated = models.DateField()
    time_updated = models.TimeField()
