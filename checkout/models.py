import uuid
from django.db import models
from django.db.models import Sum
from courses.models import Course
from user_profile.models import Discount, UserProfile
from django.conf import settings
# from bag.contexts import bag_contents

"""
Most of the logic and code taken from Boutique ADO checkout app
from code institute
"""


class Order(models.Model):
    order_number = models.CharField(default=uuid.uuid4().hex[:10].upper(),
                                    unique=True, max_length=10, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='orders')
    date = models.DateTimeField(auto_now_add=True)
    discount_percentage = models.PositiveIntegerField(null=True, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    cardholder_full_name = models.CharField(max_length=32, null=False)

    def update_total(self):
        """
        update grand_total each time a line item is added.
        Check if discount is applicable
        """
        # Getting values of discount percentage and discount threshold amount.
        # discount = Discount.objects.filter(offer_name='Discount').first()
        # discount_percentage = discount.discount_percentage
        # discount_threshold = discount.discount_amount_threshold
        
        # discount_percentage = bag_contents(request).discount_percentage
        # discount_threshold = bag_contents(request).discount_threshold

        self.order_total = self.lineitems.aggregate(Sum('course_price'))[
            'course_price__sum'] or 0
        if self.order_total > discount_threshold:
            self.grand_total = self.order_total * (1 - discount_percentage/100)
            self.discount_percentage = discount_percentage
        else:
            self.grand_total = self.order_total

        self.save()

    def __str__(self):
        return str(self.order_number)


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE,
                              related_name='lineitems')
    
    course = models.ForeignKey(Course, null=False, blank=False,
                               on_delete=models.CASCADE)
    course_price = models.PositiveIntegerField(null=False, blank=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set course price.
        """
        self.course_price = self.course.price 
        # getting current course price from the course.
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.course.title} order with order number- {self.order.order_number}'
