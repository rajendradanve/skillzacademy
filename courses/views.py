from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.contrib import messages
from django.db.models import Q
from .models import Course, CourseSchedule, MainCategory, Category
from django.db.models.functions import Lower
from user_profile.models import UserProfile
from django.contrib.auth.models import User
from django.utils import timezone

import datetime


def all_courses(request):
    """ A view to show all courses including sorting and search queries"""

    courses = Course.objects.filter(start_date__gt=datetime.date.today())

    query = None
    category = None
    categories = None
    main_category = None

    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'title':
                sortkey = 'lower_title'
                courses = courses.annotate(lower_title=Lower('title'))
            if sortkey == 'category':
                sortkey = 'category__name'
            
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
                    
            courses = courses.order_by(sortkey)
        
        # sorting based on categories in main-nav items
  
        if 'category' in request.GET:
            category = request.GET['category']
            courses = courses.filter(category__name=category)
            categories = Category.objects.filter(name=category)

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

    current_sorting = f'{sort}_{direction}'
    context = {
        'courses': courses,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'courses/courses.html', context)


def course_detail(request, course_id):
    """ A view to show individual course details"""

    course = get_object_or_404(Course, pk=course_id)
    course_schedule_list = CourseSchedule.objects.filter(course_id__pk=course.id).order_by('course_date')

    if course_schedule_list.first().course_date <= datetime.date.today():
        return redirect(reverse('courses'))

    already_in_cart = False

    if 'bag' in request.session:
        if course_id in request.session['bag']:
            already_in_cart = True

    already_bought = False
    if request.user.is_authenticated:
        # Checking orders from logged in users and checking if course is already bought.
        profile = get_object_or_404(UserProfile, user=request.user)
        if profile.orders.filter(lineitems__course_id=course_id):
            already_bought = True

    context = {
        'course': course,
        'course_schedule_list': course_schedule_list,
        'already_in_cart': already_in_cart,
        'already_bought': already_bought,


    }

    return render(request, 'courses/course_detail.html', context)