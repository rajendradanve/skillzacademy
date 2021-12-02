# This code is taken from Boutique Ado project from Code Institute.
from django.http import HttpResponse


class StripeWH_Handler:
    """ Handle Stripe webhooks"""
    
    def __init__(self, request):
        self.request = request
        
    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpectd webhook event 
        """
        
        return HttpResponse(
            content=f'Unhandled Webhook received: { event["type"]}',
            status=200)
        
    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment intent succeeded webhook from stripe 
        """
        
        return HttpResponse(
            content=f'Webhook received: { event["type"]}',
            status=200)
        
    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment intent failed webhook from stripe 
        """
        
        return HttpResponse(
            content=f'payment failed Webhook received: { event["type"]}',
            status=200)
        