from django.contrib import admin
from .models import Discount, UserProfile


class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        'offer_name',
        'discount_percentage',
        'discount_amount_threshold',
    )


admin.site.register(Discount, DiscountAdmin)


admin.site.register(UserProfile)
