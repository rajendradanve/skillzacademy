"""
View for ContactUs app
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm


def contact_us(request):
    """
    Conctact Us View
    """

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print("form valid")
            form.save()
            messages.success(request, 'Your message submitted successfully. \
                We will come back to you as soon as possible.')
            return redirect('home')
        else:
            print("form not valid")
            print(form.errors)

    form = ContactForm()

    template = 'contact_us/contact_us.html'
    context = {
        'form': form
        }
    return render(request, template, context)
