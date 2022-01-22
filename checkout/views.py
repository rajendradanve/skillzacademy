"""
View for checkout app
"""
import json
from django.shortcuts import (render, redirect, reverse,
                              get_object_or_404, HttpResponse)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
import stripe
from bag.contexts import bag_contents
from user_profile.models import UserProfile
from courses.models import Course
from .models import OrderLineItem, Order
from .forms import OrderForm


@require_POST
def cache_checkout_data(request):
    """
    Checking issue with project
    """
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'username': request.user.email,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    """
    checkout view
    """
    if not request.user.is_authenticated:
        return redirect(reverse('home'))

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', [])

        form_data = {
            'cardholder_full_name': request.POST['cardholder_full_name'],
        }

        order_form = OrderForm(form_data)

        if order_form.is_valid():

            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.save()
            for course_id in bag:
                try:
                    course = get_object_or_404(Course, pk=course_id)
                    order_line_item = OrderLineItem(order=order,
                                                    course=course,)

                    order_line_item.save()
                except Course.DoesNotExist:
                    messages.error(request, (
                        "One of the course in your bag wasn't found in our \
                        database. "
                        "Please send details of the course through our contact \
                        form")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            return redirect(reverse('checkout_success',
                                    args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with data. \
                Please double check your information.')
    else:
        bag = request.session.get('bag', [])
        if not bag:
            messages.error(request,
                           "There's nothing in your bag at the moment")
            return redirect(reverse('courses'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)

        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request,
                         'Stripe public key is missing. Did you forget to set \
                         it in your environment?')

    template = 'checkout/checkout.html'

    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    order = get_object_or_404(Order, order_number=order_number)
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        user_email = profile

        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

    else:
        messages.info(request, 'Log in before you finish purchase')
        return redirect(reverse('account_signup'))

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}.  \
         A confirmation email will be sent to register email:  { user_email }')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'user_email': user_email,
    }

    return render(request, template, context)
