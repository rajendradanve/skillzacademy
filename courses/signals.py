# Taken from Botique ADO project from code institute.

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import CourseSchedule, Course


@receiver(post_save, sender=CourseSchedule)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update start date of the course
    """
    instance.course.update_start_date()
    instance.courseschedule.update_timestamp()
    


@receiver(post_delete, sender=CourseSchedule)
def update_on_delete(sender, instance, **kwargs):
    """
    Update start date of the course
    """
    instance.course.update_start_date()
    