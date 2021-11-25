from django.db import models


class Discount(models.Model):
    offer_name = models.CharField(max_length=100)
    discount_percentage = models.PositiveIntegerField()
    discount_amount_threshold = models.PositiveIntegerField()
    
    def __str__(self):
        return self.offer_name
