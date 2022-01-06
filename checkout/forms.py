# Taken from Botique ADO project from code institute.
from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('cardholder_full_name',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholder and classes, remove auto-generated lables and set 
        autofocus on first field
        """

        super().__init__(*args, **kwargs)

        placeholders = {
            'cardholder_full_name': 'Cardholder Full Name',
        }

        self.fields['cardholder_full_name'].widget.attrs['autofocus'] = True

        for field in self.fields:
            placeholder = f'{placeholders[field]} *'
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
