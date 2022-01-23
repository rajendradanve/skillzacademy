""" Home Model """
from django.db import models


class Subscription(models.Model):
    """ Subscription Model """
    email = models.EmailField(max_length=254, null=False, blank=False)

    def __str__(self):
        return self.email
