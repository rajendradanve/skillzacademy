from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Subscription
from django.contrib import messages


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


