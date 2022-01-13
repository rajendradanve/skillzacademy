from django.contrib import admin
from .models import Subscription, Contact

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
    )
    
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'subject',
    )

admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Contact, ContactAdmin)