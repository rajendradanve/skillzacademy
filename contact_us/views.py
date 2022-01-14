from django.shortcuts import render
from .models import ContactUs
from django.contrib import messages
from .forms import ContactForm


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