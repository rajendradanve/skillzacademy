from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.contrib import messages
from django.db.models import Q
from .models import Course, CourseSchedule, MainCategory, Category

# Create your views here.


def all_courses(request):
    """ A view to show all courses including sorting and search queries"""
    courses = Course.objects.all()
    query = None
    category = None
    main_category = None
    
    # sorting based on categories in main-nav items
    if request.GET:
        if 'category' in request.GET:
            category = request.GET['category']
            courses = courses.filter(category__name=category)
            
    # sorting based on all courses for top main-nav item
        if 'main_category' in request.GET:
            main_category = request.GET['main_category']
            
            categories = Category.objects.filter(main_category__name=main_category)
            
            courses = courses.filter(category__in=categories)
            
    if request.GET:
        if 'q' in request.GET:
            
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
        'current_category': category,
        'main_category': main_category,
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