# This code is taken from Boutique Ado project from Code Institute.
from django.http import HttpResponse


class StripeWH_Handler:
    """ Handle Stripe webhooks"""
    
    def __init__(self, request):
        self.request = request
        
    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpectd webhook evnt 
        """
        
        return HttpResponse(
            content = f'Webhook received: { event["type"]}',
            status= 200)