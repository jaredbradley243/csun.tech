from django.shortcuts import render

# Create your views here.
<<<<<<< Updated upstream
=======


def index(request):
    return HttpResponse("Hello, world. You're at the index.")


# todo - save the form when the email is received and the link is clicked
def register(request):
    form = CustomRegistrationForm()

    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid:
            user = form.save(commit=False)
            user.is_active = False
            user_email = user.email
            if user_email.endswith("@csun.edu"):
                user.is_professor = True
            elif user_email.endswith("@my.csun.edu"):
                user.is_student = True
            else:
                return HttpResponse("Please enter a CSUN email!")
            print(
                "user email: \n",
                user_email,
                "\n username: \n",
                user.username,
                "\n first name: \n",
                user.first_name,
                "\n last name: \n",
                user.last_name,
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
>>>>>>> Stashed changes
