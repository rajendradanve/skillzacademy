from django.shortcuts import render
from .models import Course, CourseSchedule

# Create your views here.


def all_courses(request):
    """ A view to show all courses including sorting and search queries"""
    
    courses = Course.objects.all()
    
    context = {
        'courses': courses,
        
    }
    
    return render(request, 'courses/course.html', context)
