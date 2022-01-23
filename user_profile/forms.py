from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import User
from .models import Discount


class CustomSignupForm(SignupForm):
    """
    Custom signup form extension to allauth signup form.
    Added First and Last name
    """
    first_name = forms.CharField(max_length=30, label='First Name',
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, label='Last Name',
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    
    class Meta:
        model = User()
        fields = ['first_name', 'last_name']
        fields = ('first_name', 'last_name')
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['offer_name'].label = 'Offer Name'
        self.fields['offer_flag'].label = 'Offer Active'
        self.fields['offer_flag'].required = False
        self.fields['discount_amount_threshold'].label = 'Discount Amount Threshold in $'
    
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-dark rounded-1'
            
