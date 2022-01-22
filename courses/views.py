"""
Views for Courses app
"""
import datetime
from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower
from django.forms import inlineformset_factory
from user_profile.models import UserProfile
from .models import Course, CourseSchedule, MainCategory, Category
from .forms import (CategoryForm, MainCategoryForm, UpdateCategoryForm,
                    CourseForm, CourseScheduleForm)



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
    course_schedule_list = CourseSchedule.objects.filter(
        course_id__pk=course.id).order_by('course_date')

    if course_schedule_list.first().course_date <= datetime.date.today():
        return redirect(reverse('courses'))

    already_in_cart = False

    if 'bag' in request.session:
        
        if course_id in request.session['bag']:
            already_in_cart = True
            print(course_id)
    
    print(already_in_cart)
    
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


@login_required
def add_course(request):
    """ Add new course"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin can visit this page.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)

        if form.is_valid():
            new_course = form.save()
            new_course_id = new_course.id
            return redirect('add_course_schedule', course_id=new_course_id)
        else:
            messages.error(request, 'Failed to add course. Check all values are filed correctly.')

    form = CourseForm()

    template = 'courses/add_course.html'

    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def add_course_schedule(request, course_id):
    """
    method to add course schedule
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin can visit this page.')
        return redirect(reverse('home'))

    course = Course.objects.get(pk=course_id)

    AddCourseScheduleFormset = inlineformset_factory(Course, CourseSchedule,
                                                     form=CourseScheduleForm, extra=1)

    if request.method == 'POST':

        formset = AddCourseScheduleFormset(request.POST, instance=course)
        if formset.is_valid():
            formset.save()

            if 'save-n-add' in request.POST:
                
                return redirect('add_course_schedule', course_id=course.id)
            elif 'save-n-view' in request.POST:
                messages.success(request, 'Course updated successfully')
                return redirect('course_detail', course_id=course.id)
        else:

            messages.error(request, 'Something went wrong. Please try again')

    formset = AddCourseScheduleFormset(instance=course)

    template = 'courses/add_course_schedule.html'
    context = {
        'formset': formset,
        'course_id': course_id,
        'from_course_detail': False,
    }
    return render(request, template, context)


@login_required
def update_course_schedule(request, course_id):
    """
    method to update course schedule
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin can visit this page.')
        return redirect(reverse('home'))

    course = Course.objects.get(pk=course_id)

    AddCourseScheduleFormset = inlineformset_factory(Course, CourseSchedule,
                                                     form=CourseScheduleForm, extra=0)

    if request.method == 'POST':
        formset = AddCourseScheduleFormset(request.POST, instance=course)
        
        if formset.is_valid():
            formset.save()

            if 'save-n-add' in request.POST:
                return redirect('add_course_schedule', course_id=course.id)
            elif 'save-n-view' in request.POST:
                messages.success(request, 'Course schedule update successfully')
                return redirect('course_detail', course_id=course.id)
            else:
                messages.error(request, 'Something went wrong. Please try again')
                
    formset = AddCourseScheduleFormset(instance=course)
    template = 'courses/add_course_schedule.html'
    context = {
        'formset': formset,
        'course_id': course_id,
        'from_course_detail': True,
    }
    return render(request, template, context)


@login_required
def add_category(request):
    """ Add new category"""

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin visit this page.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            friendly_name = request.POST['friendly_name']
            name = request.POST['friendly_name'].lower().replace(' ',  '_')

            if Category.objects.filter(friendly_name=friendly_name).exists(
                ) or Category.objects.filter(name=name).exists():
                messages.warning(request,
                                 (f'{friendly_name} already exists in the database. '
                                  'Please enter another name'
                                  ))
                return redirect(reverse('add_category'))
            else:
                form.save()
                messages.success(request,
                                 (f'{friendly_name} added in the database.'))
                return redirect('admin')

    add_category_form = CategoryForm()
    template = 'courses/add_category.html'

    context = {
        'add_category_form': add_category_form,
    }
    return render(request, template, context)


@login_required
def add_main_category(request):
    """ Add new main category"""

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin visit this page.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = MainCategoryForm(request.POST)
        if form.is_valid():
            friendly_name = request.POST['friendly_name']
            name = request.POST['friendly_name'].lower().replace(' ',  '_')

            if MainCategory.objects.filter(friendly_name=friendly_name).exists(
                ) or Category.objects.filter(name=name).exists():
                messages.warning(request,
                                 (f'{friendly_name} already exists in the database. '
                                  'Please enter another name'
                                  ))
                return redirect(reverse('add_main_category'))
            else:
                form.save()
                messages.success(request,
                                 (f'{friendly_name} added in the database.'))
                return redirect('admin')

    template = 'courses/add_main_category.html'
    add_main_category_form = MainCategoryForm()
    context = {
        'add_main_category_form': add_main_category_form,

    }
    return render(request, template, context)


@login_required
def select_category(request):
    """ Choose category to update"""

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin can visit this page.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        category_id = request.POST['select-category']
        return redirect('update_category', category_id=category_id)

    categories = Category.objects.all()
    template = 'courses/select_category.html'

    context = {
        'categories': categories,
    }
    return render(request, template, context)


@login_required
def update_category(request, category_id):
    """ Update category"""

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin can visit this page.')
        return redirect(reverse('home'))

    category = get_object_or_404(Category, pk=category_id)

    if request.method == 'POST':
        update_category_form = UpdateCategoryForm(request.POST, instance=category)

        if update_category_form.is_valid():
            update_category_form.save()
            messages.success(request, (
                'You successfully updated category in the database.'
                ))
            return redirect('admin')
    else:
        update_category_form = UpdateCategoryForm(instance=category)
        messages.info(request, f'You are editing {category.friendly_name}')

    template = 'courses/update_category.html'

    context = {
        'update_category_form': update_category_form,
        'category': category,
    }
    return render(request, template, context)


@login_required
def update_main_category(request):
    """ Update category"""

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin can visit this page.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        MainCategory.objects.filter(pk=request.POST['select-main-category']
                                    ).update(friendly_name=request.POST['new-main-category'])
        messages.success(request, (
            'You successfully updated category name in the database.'
            ))
        return redirect('admin')
    else:
        main_categories = MainCategory.objects.all()

    template = 'courses/update_main_category.html'

    context = {
        'main_categories': main_categories,
    }
    return render(request, template, context)


@login_required
def delete_course(request, course_id):
    """ Delete a Course """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin can update database')
        return redirect(reverse('home'))

    course = get_object_or_404(Course, pk=course_id)
    course.delete()
    messages.success(request, (f'{ course.title }deleted successfully'))
    return redirect(reverse('admin'))


@login_required
def update_course(request, course_id):
    """ Update course data """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin can update database')
        return redirect(reverse('home'))
    
    course = get_object_or_404(Course, pk=course_id)

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated course!')
            return redirect(reverse('course_detail', args=[course.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form \
                information is correct.')

    else:
        form = CourseForm(instance=course)

    template = 'courses/update_course.html'

    context = {
        'form': form,
        'course': course,
        'from': 'update',
    }
    return render(request, template, context)
