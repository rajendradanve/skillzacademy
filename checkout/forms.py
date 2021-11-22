# Taken from Botique ADO project from code institute.
from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = order
        fields = ('full_name', 'email',)
        
    
    def __init__(self, *args, **kwargs):
        """
        Add placeholder and classes, remove auto-generated lables and set autofocus on first field
        """
        
        super().__init__(*args, **kwargs):
        
        placeholder = {
            'full_name': 'Full Name',
            'email': 'Email Address',
        }
        
        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            placeholder = f'{placeholder[field]} *'
        
            self.fields[field].widget.attrs['placeholder']=placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].lables = False
                