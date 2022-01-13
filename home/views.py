from django.shortcuts import render
from .models import Subscription
# Create your views here.


def index(request):
    """ A view to return the index page"""
    
    return render(request, 'home/index.html')

def subscribe(request):

    if(reqest.method == 'POST'):
        email = request.POST.get('subscription-email')
        Subscription.create(email=email)
        return HttpResponseRedirect(request.path_info)