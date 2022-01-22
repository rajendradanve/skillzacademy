import json
import time

from django.http import HttpResponse,request
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from courses.models import Course
from .models import Order, OrderLineItem
from user_profile.models import UserProfile

class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request
        

    def _send_confirmation_email(self, order):
        """
        Send the user a confirmation email about order
        """
        cust_email = "rajendradanve@gmail.com"
        
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        print(f'stripe intent= {intent}')
        billing_details = intent.charges.data[0].billing_details
        grand_total = round(intent.charges.data[0].amount/100, 2)
        print(f'billing_details={billing_details}')
        username = intent.metadata.username
        profile = UserProfile.objects.get(user__email=username)
        order_exists = False
        attempt = 1
        print(f'profile = {profile}')
        while attempt <=5:
            try:
                order = Order.objects.get(
                    user_profile=profile,
                    cardholder_full_name__iexact=billing_details.name,
                    grand_total=grand_total,
                    stripe_pid=pid,
                )
                order_exists = True
                print(f'attempt={attempt} + order = {order.order_number}')
                break
            except Order.DoesNotExist:
                attempt += 1
                print(f'attempt = {attempt}')
                time.sleep(1)

        if order_exists:
            print(f'Order exists after while={order}')
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]}| SUCCESS: \
                VERIFIED order already in database ',
                    status=200)

        else:
            order = None
            try:
                
                order = Order.objects.create(
                        cardholder_full_name=billing_details.name,
                        stripe_pid=pid,
                        user_profile= profile
                    )

                for course_id in json.loads(bag):
                    course = Course.objects.get(id=course_id)
                    order_line_item = OrderLineItem(order=order,
                                                        course=course,)
                    order_line_item.save()
            except Exception as e:
                print(e)
                if order:
                    order.delete()
                return HttpResponse(content=f'Webhook received: {event["type"]}|\
                    ERROR: {e}',status=500)
        self._send_confirmation_email(order)
        print(f'Order exists2nd={order}')
        return HttpResponse(content=f'Webhook received: {event["type"]}',status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
