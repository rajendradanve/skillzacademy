"""
View for ContactUs app
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .forms import ContactForm


def contact_us(request):
    """
    Contact Us View
    """

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            contact_email = request.POST.get('contact_email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            send_mail(
                subject,
                message,
                contact_email,
                [settings.ADMIN_EMAIL]
                )

            messages.success(request, 'Your message submitted successfully. \
                We will come back to you as soon as possible.')
            return redirect('home')
        else:
            messages.success(request, 'Error occured while submitting the form. Try again.')
            return redirect(reversed('contact_us'))
    form = ContactForm()

    template = 'contact_us/contact_us.html'
    context = {
        'form': form
        }
    return render(request, template, context)
