from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Subscription
from django.contrib import messages
from .forms import ContactForm

def home(request):
    """ A view to return the home page"""
    
    return render(request, 'home/index.html')


def subscribe(request):

    if(request.method == 'POST'):
        email = request.POST.get('subscription-email')
  
        if Subscription.objects.filter(email=email).exists():
            messages.info(request, (f'{email} already exist in the subscription list'))
        else:
            Subscription.objects.create(email=email).save()
            messages.success(request, (f'{email} added in the subscription list'))
        
        return HttpResponseRedirect(request.path_info)


    return redirect(request.META['HTTP_REFERER'])


def contact_us(request):

    if request.method == 'POST':
       # print(request.POST)
        form = ContactForm(request.POST)
        if form.is_valid():
            print("form valid")
            form.save()
            messages.success(request, 'Your message submitted successfully. We will come back to you as soon as possible.')
            return redirect(reverse('home'))
        else:
            print("form not valid")
            print(form.errors)
            
    form = ContactForm()

    template = 'home/contact_us.html'
    context = {
        'form': form
        }
    return render(request, template, context)