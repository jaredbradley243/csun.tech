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
            user.is_active = False
            user_email = user.email
            if user_email.endswith("@csun.edu"):
                user.is_professor = True
            elif user_email.endswith("@my.csun.edu"):
                user.is_student = True
            else:
                return HttpResponse("Please enter a CSUN email!")
            if user.is_student:
                if not user.student_id:
                    return HttpResponse("Please enter your student ID")
            if len(user.student_id) != 9:
                return HttpResponse("Please enter a valid student ID")
            print(
                "user email: \n",
                user_email,
                "\n username: \n",
                user.username,
                "\n first name: \n",
                user.first_name,
                "\n last name: \n",
                user.last_name,
                "\n student id: \n",
                user.student_id,
                "\n Is professor: \n",
                user.is_professor,
                "\n Is student: \n",
                user.is_student,
                "\n is active: \n",
                user.is_active,
                "\n is staff: \n",
                user.is_staff,
                "\n email confirmed: \n",
                user.email_confirmed,
            )
            send_mail(
                subject="Register Your Account With CSUN.tech",
                message="Please register your account to continue.",
                from_email="no-reply@csun.tech",
                recipient_list=[user_email],
                fail_silently=True,
            )

    return render(request, "accounts/register.html", {"form": form})
