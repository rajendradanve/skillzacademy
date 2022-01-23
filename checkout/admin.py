"""
Admin for checkout app
"""
from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    """
    Order line item to show list under specific order
    """
    model = OrderLineItem
    readonly_fields = ('course_price',)


class OrderAdmin(admin.ModelAdmin):
    """
    OrderAdmin
    """
    inlines = (OrderLineItemAdminInline,)
    readonly_fields = ('order_number', 'date', 'user_profile',
                       'discount_percentage', 'order_total', 'grand_total',
                       'cardholder_full_name', 'stripe_pid')

    fields = ('order_number', 'date', 'user_profile', 'discount_percentage',
              'order_total', 'grand_total', 'cardholder_full_name',
              'stripe_pid')

    list_display = ('order_number', 'date', 'user_profile',
                    'grand_total', 'cardholder_full_name', 'stripe_pid')

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
