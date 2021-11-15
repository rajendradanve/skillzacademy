from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from courses.models import Course
# Create your views here.


def view_bag(request):
    """ A view that renders the bag contents page """
    
    return render(request, 'bag/bag.html')


def add_to_bag(request, course_id):
    """ Add a course to the bag """
    
    course = Course.objects.get(pk=course_id)
    
    redirect_url = request.POST.get('redirect_url')
    
    bag = request.session.get('bag', [])
    
    bag.append(course_id)
    
    request.session['bag'] = bag
    messages.success(request, f'Added {course.title} to your bag')
    return redirect(redirect_url)


def remove_course_from_bag(request, course_id):
    """ Adjust the bag view a course to the bag """
    
    bag = request.session.get('bag', [])
    
    bag.remove(course_id)
    
    request.session['bag'] = bag
    
    return redirect(reverse('view_bag',))
