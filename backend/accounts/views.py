from email.message import EmailMessage
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail


# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the index.")


def register(request):
    return HttpResponse("Hello, world. You're at the register page.")
