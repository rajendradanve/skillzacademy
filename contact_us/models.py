"""
Contact Us Model
"""
from django.db import models


class ContactUs(models.Model):
    """
    Model for contact us
    """
    full_name = models.CharField(max_length=100, null=False, blank=False)
    contact_email = models.EmailField(null=False, blank=False)
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.contact_email
