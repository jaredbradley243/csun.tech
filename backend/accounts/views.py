from email.message import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the index.")


def register(request):
    send_mail(
        subject="Register Your Account With CSUN.tech",
        message="Please register your account to continue.",
        from_email="no-reply@csun.tech",
        recipient_list=["user@gmail.com"],
        fail_silently=True,
    )
    return HttpResponse("Hello, world. You're at the register page.")
