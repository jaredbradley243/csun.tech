from email.message import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from accounts.forms import CustomRegistrationForm


# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the index.")


def register(request):
    form = CustomRegistrationForm()

    send_mail(
        subject="Register Your Account With CSUN.tech",
        message="Please register your account to continue.",
        from_email="no-reply@csun.tech",
        recipient_list=["TestUser@gmail.com"],
        fail_silently=True,
    )

    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        print(form.data)

    return render(request, "accounts/register.html", {"form": form})
