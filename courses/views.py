from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.contrib import messages
from django.db.models import Q
from .models import Course, CourseSchedule

# Create your views here.


def all_courses(request):
    """ A view to show all courses including sorting and search queries"""
    courses = Course.objects.all()
    query = None
    if request.GET:
        if 'q' in request.GET:
            print("test")
            query = request.GET['q']
            if not query:
                messages.error(request, "Please enter search criteria!")
                return redirect(reverse('courses'))
            # Created queries with 'or' condition
            queries = Q(title__icontains=query) | Q(description__icontains=query)
            
            courses = courses.filter(queries)
    
    context = {
        'courses': courses,
        'search_term': query,
        
    }
    
    return render(request, 'courses/courses.html', context)


def course_detail(request, course_id):
    """ A view to show individual course details"""
    
    course = get_object_or_404(Course, pk=course_id)
    course_schedule = CourseSchedule.objects.filter(course_id__pk=course.id).order_by('course_date')
    

    context = {
        'course': course,
        'course_schedule': course_schedule,
        
    }
    
    return render(request, 'courses/course_detail.html', context)