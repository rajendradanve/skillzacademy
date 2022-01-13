from django.db import models


class Subscription(models.Model):
    email = models.EmailField(max_length=254, null=False, blank=False)
    

class Contact(models.Model):
    name = models.CharField(max_length= 100, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.email