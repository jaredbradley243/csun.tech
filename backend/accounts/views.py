from email.message import EmailMessage
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from accounts.forms import CustomRegistrationForm


# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the index.")


def register(request):
    form = CustomRegistrationForm()

    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # * is_active is set to False to prevent users from logging in
            # * until they confirm their email
            user.is_active = False
            user_email = user.email
            if user_email.endswith("@csun.edu"):
                user.is_professor = True
            elif user_email.endswith("@my.csun.edu"):
                user.is_student = True
            else:
                return HttpResponse("Please enter a CSUN email!")
            print(user.is_student, user.student_id)
            if user.is_student:
                if not user.student_id:
                    return HttpResponse("Please enter your student ID")
            if len(user.student_id) != 9:
                return HttpResponse("Please enter a valid student ID")

            send_mail(
                subject="Register Your Account With CSUN.tech",
                message="Please register your account to continue.",
                from_email="no-reply@csun.tech",
                recipient_list=[user_email],
                fail_silently=True,
            )
            # ! Uncomment the line below to save the user to the database
            # ! after email confirmation is implemented and business logic is
            # ! finalized
            # user.save()
        else:
            # * If the form is not valid, return the error message
            error_message = form.errors.as_text()
            return HttpResponse(error_message)

    return render(request, "accounts/register.html", {"form": form})
