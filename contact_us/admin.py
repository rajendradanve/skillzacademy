"""
admin for contact us
"""
from django.contrib import admin
from .models import ContactUs


class ContactUsAdmin(admin.ModelAdmin):
    """
    ContactUsAdmin
    """
    list_display = (
        'full_name',
        'contact_email',
        'subject',
    )


admin.site.register(ContactUs, ContactUsAdmin)
