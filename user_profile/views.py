from django.shortcuts import render

# Create your views here.


def profile(request):
    """ A view to return the index page"""

    return render(request, 'user_profile/profile.html')


def admin_profile(request):
    """ A view to return the index page"""

    return render(request, 'user_profile/admin.html')

def add_course(request):
    """ A view to return the index page"""

    return render(request, 'user_profile/add_course.html')
