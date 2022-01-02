from django.shortcuts import render
from courses.models import Course, Category, MainCategory
# Create your views here.


def profile(request):
    """ To use profile of the normal user."""

    return render(request, 'user_profile/profile.html')


def admin_profile(request):
    """ Admin Profile Page"""

    return render(request, 'user_profile/admin.html')


def add_course(request):
    """ Add new course"""

    return render(request, 'user_profile/add_course.html')


def add_category(request):
    """ Add new category"""
        
    main_categories = MainCategory.objects.all()
    
    context = {
        'main_categories': main_categories,
    }
    return render(request, 'user_profile/add_category.html', context)


def add_main_category(request):
    """ Add new main category"""

    return render(request, 'user_profile/add_main_category.html')


def purchase_history(request):
    """ Showing Purchase History of the Courses """
    
    return render(request, 'user_profile/purchase_history.html')