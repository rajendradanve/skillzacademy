"""
Form for Contact Us Page
"""
from django import forms
from .models import ContactUs


class ContactForm(forms.ModelForm):
    """
    Contact Us form
    """
    class Meta:
        model = ContactUs
        fields = ['full_name', 'contact_email', 'subject', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-dark rounded-1'
            field.widget.attrs['required'] = 'required'