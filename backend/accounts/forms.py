from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser


class CustomRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "student_id",
        ]

    def __init__(self, *args, **kwargs):
        super(CustomRegistrationForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"placeholder": "Email"})
        self.fields["first_name"].widget.attrs.update({"placeholder": "First Name"})
        self.fields["last_name"].widget.attrs.update({"placeholder": "Last Name"})
        self.fields["student_id"].widget.attrs.update({"placeholder": "Student ID"})
