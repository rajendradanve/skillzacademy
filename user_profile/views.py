from django.shortcuts import render, get_object_or_404, redirect
from courses.models import Course, Category, MainCategory
from checkout.models import Order
from .models import UserProfile
from django.contrib import messages
from .forms import CategoryForm

def admin_profile(request):
    """ Admin Profile Page"""

    return render(request, 'user_profile/admin.html')


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


def add_course(request):
    """ Add new course"""

    return render(request, 'user_profile/add_course.html')


def add_category(request):
    """ Add new category"""

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin')

    add_category_form = CategoryForm()
    template = 'user_profile/add_category.html'
    
    context = {
        'add_category_form': add_category_form,
    }
    return render(request, template, context)


def add_main_category(request):
    """ Add new main category"""

    return render(request, 'user_profile/add_main_category.html')


def purchase_history(request):
    """ Showing Purchase History of the Courses """
    profile = get_object_or_404(UserProfile, user=request.user)
    orders = profile.orders.all()

    template = 'user_profile/purchase_history.html'
    context = {
        'orders': orders,
    }
    return render(request, template, context)


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
