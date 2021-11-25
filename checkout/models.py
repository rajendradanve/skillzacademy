import uuid
from django.db import models
from django.db.models import Sum
from courses.models import Course
from bag.contexts import bag_contents
# Create your models here.
# Taken from Boutique ADO checkout app from code institute

class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    discount_percentage = models.PositiveIntegerField(null=True, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    cardholder_full_name = models.CharField(max_length=32, null=False)
    
    
    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()
    
    def update_total(self):
        """
        update grand_total each time a line item is added.
        Check if discount is applicable
        """
        self.discount_percentage = bag_contents.discount_percentage
        self.order_total = self.lineitems.aggregate(Sum('course_price'))['course_price__sum'] or 0
        if self.order_total > bag_contents.discount_threshold:
            self.grand_total = self.order_total * (1 - bag_contents.discount_percentage/100)
        else:
            self.grand_total = self.order_total
        
        self.save()
    
    def save(self, *args, **kwargs):
        """ 
        Override the original save method to set the order number if it hasn't been set already
        """
        
        if not self.order_number:
            self.order_number = self._generate_order_number()
            super().save(*args, **kwargs)
            
    def __str__(self):
        return self.order_number

class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    course = models.ForeignKey(Course, null=False, blank=False, on_delete=models.CASCADE)
    course_price = models.PositiveIntegerField(null=False, blank=False)
    
    def save(self, *args, **kwargs):
        """
        Override the original save method to set course price and update the order total
        """
        self.course_price = self.course.price # getting current course price from the course.
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.course.title} order with order number- {self.order.order_number}'
    