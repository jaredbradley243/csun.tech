from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.core.validators import (
    FileExtensionValidator,
    MinLengthValidator,
    MaxLengthValidator,
)
from django.forms import ValidationError


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValidationError("Please enter an email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if email.endswith("@csun.edu"):
            user.is_professor = True
        elif email.endswith("@my.csun.edu"):
            user.is_student = True
        else:
            raise ValidationError("Please use your CSUN email address")
        if user.is_student:
            if not user.student_id:
                raise ValidationError("Please enter your student ID")
        if len(user.student_id) != 9:
            raise ValidationError("Please enter a valid student ID")
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, email, first_name, last_name, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields["first_name"] = first_name
        extra_fields["last_name"] = last_name
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


# * CustomUser is for user information related to authentication and user roles
class CustomUser(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=False)
    username = models.CharField(max_length=150, unique=True, default="")
    first_name = models.CharField(max_length=30, blank=False, verbose_name="first name")
    last_name = models.CharField(max_length=30, blank=False, verbose_name="last name")
    student_id = models.CharField(
        unique=True,
        max_length=9,
        blank=False,
        validators=[MinLengthValidator(9), MaxLengthValidator(9)],
        verbose_name="Student ID",
    )
    is_staff = models.BooleanField(default=False, verbose_name="staff")
    is_professor = models.BooleanField(default=False, verbose_name="professor")
    is_team_lead = models.BooleanField(default=False, verbose_name="team lead")
    is_student = models.BooleanField(default=False, verbose_name="student")
    email_confirmed = models.BooleanField(default=False, verbose_name="email confirmed")
    is_active = models.BooleanField(default=True, verbose_name="active")

    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    # For createsuperuser commands
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)


# * UserProfile is for user information not related to authentication or user roles
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_volunteer = models.BooleanField(default=False)
    resume = models.FileField(
        upload_to="resumes/",
        validators=[FileExtensionValidator(["pdf"])],
        null=True,
        blank=True,
    )

    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
