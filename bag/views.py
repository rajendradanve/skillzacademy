from django.shortcuts import render, redirect

# Create your views here.


def view_bag(request):
    """ A view that renders the bag contents page """
    
    return render(request, 'bag/bag.html')


def add_to_bag(request, course_id):
    """ Add a course to the bag """
    
    redirect_url = request.POST.get('redirect_url')
    
    bag = request.session.get('bag', [])
    
    bag.append(course_id)
    
    request.session['bag'] = bag

    
    return redirect(redirect_url)
