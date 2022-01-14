from django.contrib import admin
from .models import ContactUs

# Register your models here.
class ContactUsAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'contact_email',
        'subject',
    )
    

admin.site.register(ContactUs, ContactUsAdmin)