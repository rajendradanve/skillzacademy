""" Views for user_profile app """
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from checkout.models import Order
from .models import UserProfile, Discount
from .forms import DiscountForm


def admin_profile(request):
    """ Admin Profile Page"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin can visit this page.')
        return redirect(reverse('home'))

    return render(request, 'user_profile/admin.html')


@login_required
def my_courses(request):
    """ Showing List of Register Courses"""

    profile = get_object_or_404(UserProfile, user=request.user)
    orders = profile.orders.all()
    courses = []
    for order in orders:

        for item in order.lineitems.all():
            courses.append(item.course)

    template = 'user_profile/my_courses.html'

    context = {

        'courses': courses,
    }

    return render(request, template, context)


@login_required
def purchase_history(request):
    """ Showing Purchase History of the Courses """
    profile = get_object_or_404(UserProfile, user=request.user)
    orders = profile.orders.all()

    template = 'user_profile/purchase_history.html'
    context = {
        'orders': orders,
    }
    return render(request, template, context)


@login_required
def purchase_history_details(request, order_number):
    """ Showing purchase history details based on order number to the user """
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'

    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


@login_required
def discount(request):
    """
    View to edit or update discount.
    """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin can visit this page.')
        return redirect('home')

    discount0 = Discount.objects.first()

    if request.method == 'POST':
        if discount:
            form = DiscountForm(request.POST, instance=discount0)
        else:
            form = DiscountForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request,
                             'Discount data added in the database.')

            return redirect('admin')
        else:
            messages.error(request,
                           'Something went wrong. Try again')

            return redirect(reverse('discount'))

    form_flag = 'add'
    if discount0:
        form = DiscountForm(instance=discount0)
        form_flag = 'update'
    else:
        form = DiscountForm()
        form_flag = 'add'

    template = 'user_profile/discount.html'
    context = {
        'form': form,
        'form_flag': form_flag,
    }

    return render(request, template, context)
