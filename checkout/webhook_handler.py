"""
Webhook handler to manage handler event from stripe.
"""
import json
import time

from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from user_profile.models import UserProfile
from courses.models import Course
from .models import Order, OrderLineItem


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request


    def _send_confirmation_email(self, order):
        """
        Send the user a confirmation email about order
        """
        cust_email = order.user_profile
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

        billing_details = intent.charges.data[0].billing_details
        grand_total = round(intent.charges.data[0].amount/100, 2)

        username = intent.metadata.username
        profile = UserProfile.objects.get(user__email=username)
        order_exists = False
        attempt = 1

        while attempt <=5:
            try:
                order = Order.objects.get(
                    user_profile=profile,
                    cardholder_full_name__iexact=billing_details.name,
                    grand_total=grand_total,
                    stripe_pid=pid,
                )
                order_exists = True

                break
            except Order.DoesNotExist:
                attempt += 1

                time.sleep(1)

        if order_exists:

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

                if order:
                    order.delete()
                return HttpResponse(content=f'Webhook received: {event["type"]}|\
                    ERROR: {e}',status=500)
        self._send_confirmation_email(order)

        return HttpResponse(content=f'Webhook received: {event["type"]}',status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
