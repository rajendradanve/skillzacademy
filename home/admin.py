""" Home admin """
from django.contrib import admin
from .models import Subscription


class SubscriptionAdmin(admin.ModelAdmin):
    """ SubscriptionAdmin """
    list_display = (
        'id',
        'email',
    )


admin.site.register(Subscription, SubscriptionAdmin)
