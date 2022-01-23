"""
Most of the logic and code taken from Boutique ADO checkout app
from code institute
"""
import uuid
from django.db import models
from django.db.models import Sum
from courses.models import Course
from user_profile.models import Discount, UserProfile


class Order(models.Model):
    """
    Create Order model
    """
    order_number = models.CharField(max_length=32, null=False, editable=False)
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
    stripe_pid = models.CharField(max_length=254, null=False,
                                  blank=False, default='')

    def _generate_order_number(self):
        """
        Generate unique order number
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        update grand_total each time a line item is added.
        Check if discount is applicable
        """

        discount_percentage = 0
        discount_threshold = 0
        discount_flag = False

        if Discount.objects.filter(offer_flag=True).exists():
            discount_flag = True
            discount = Discount.objects.filter(offer_flag=True).first()
            discount_percentage = discount.discount_percentage
            discount_threshold = discount.discount_amount_threshold

        self.order_total = self.lineitems.aggregate(Sum('course_price'))[
            'course_price__sum'] or 0
        if discount_flag:
            if self.order_total > discount_threshold:
                self.grand_total = self.order_total * (
                    1 - discount_percentage/100)
                self.discount_percentage = discount_percentage

        self.grand_total = self.order_total

        self.save()

    def __str__(self):
        return str(self.order_number)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)


class OrderLineItem(models.Model):
    """
    Create OrderLineItem model
    """
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
        return f'{self.course.title} order with order number- \
    {self.order.order_number}'
