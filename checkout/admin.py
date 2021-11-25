from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('course_price',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)
    readonly_fields = ('order_number', 'date', 'discount_percentage',
                       'order_total', 'grand_total',)

    fields = ('order_number', 'date', 'discount_percentage', 'order_total', 'grand_total',)

    list_display = ('order_number', 'date', 'discount_percentage', 'order_total', 'grand_total',)

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
