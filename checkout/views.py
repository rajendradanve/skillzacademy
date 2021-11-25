from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
import stripe
from bag.contexts import bag_contents
from courses.models import Course
from .models import OrderLineItem, Order
from .forms import OrderForm


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', [])

        form_data = {
            'cardholder_full_name': request.POST['cardholder_full_name'],
        }

        order_form = OrderForm(form_data)

        if order_form.is_valid():
            order = order_form.save()

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
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to register email')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
