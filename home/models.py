from django.db import models


class Subscription(models.Model):
    email = models.EmailField(max_length=254, null=False, blank=False)
    
