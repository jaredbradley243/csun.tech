from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.core.validators import (
    FileExtensionValidator,
    MinLengthValidator,
    MaxLengthValidator,
)

from rest_framework.exceptions import ValidationError, PermissionDenied
from csuntech.settings import AUTH_USER_MODEL
from projects.models import Project


def validate_integer(value):
    if not value.isdigit():
        raise ValidationError("Only integer values are allowed.")


class CustomUserManager(BaseUserManager):
    """
    Custom user manager to handle user creation and superuser creation with
    custom fields and validations.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValidationError("An Email Address Is Required")

        email = self.normalize_email(email)

        if not email.endswith(("@csun.edu", "@my.csun.edu")):
            raise ValidationError("Please Enter A CSUN email address")

        user = self.model(email=email, **extra_fields)

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


class CustomUser(AbstractUser):
    """
    CustomUser model extends AbstractUser and PermissionsMixin to include
    additional fields and customizations
    for user authentication and roles.
    """

    email = models.EmailField(unique=True, blank=False)
    username = models.CharField(max_length=150, unique=True, default="")
    first_name = models.CharField(max_length=30, blank=False, verbose_name="first name")
    last_name = models.CharField(max_length=30, blank=False, verbose_name="last name")
    is_staff = models.BooleanField(default=False, verbose_name="staff")
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


class UserProfile(models.Model):
    """
    UserProfile model stores additional user information not related to
    authentication or user roles.
    """

    user = models.OneToOneField(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    bio = models.TextField(null=True, blank=True)
    # Todo: Implement Photo

    @property
    def is_student(self):
        return self.user.email.endswith("@my.csun.edu")

    @property
    def is_team_lead(self):
        return self.is_student and self.team_lead

    @property
    def is_professor(self):
        return self.user.email.endswith("@csun.edu")

    @property
    def get_role(self):
        if self.is_professor:
            return "professor"
        elif self.is_team_lead:
            return "team lead"
        elif self.is_student:
            return "student"
        else:
            return "unknown"


class StudentProfile(UserProfile):
    team_lead = models.BooleanField(default=False, blank=True)
    is_volunteer = models.BooleanField(default=False, verbose_name="volunteer")
    student_id = models.CharField(
        unique=True,
        max_length=9,
        blank=False,
        validators=[MinLengthValidator(9), MaxLengthValidator(9), validate_integer],
        verbose_name="Student ID",
        null=False,
    )
    resume = models.FileField(
        upload_to="resumes/",
        validators=[FileExtensionValidator(["pdf"])],
        null=True,
        blank=True,
    )

    project = models.ForeignKey(
        "projects.Project",
        related_name="students",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    # TODO: Join_project and leave_project need to be refactored into project model
    def join_project(self, project):
        if self.project:
            raise ValidationError("You're already enrolled in a project")
        project.add_student(self)

    def leave_project(self):
        if not self.project:
            raise ValidationError("You're not enrolled in a project")
        self.project.remove_student(self)


class TeamLeadProfile(StudentProfile):
    class Meta:
        proxy = True

    def add_student_to_project(self, student):
        if not self.project:
            raise ValidationError("User is not enrolled in a project")
        self.project.add_student(student, self)

    def remove_student_from_project(self, student):
        if not self.project:
            raise ValidationError("User is not enrolled in a project")
        self.project.remove_student(student, self)


class ProfessorProfile(UserProfile):
    rate_my_professor_link = models.URLField(blank=True, null=True)
    csun_faculty_page_link = models.URLField(blank=True, null=True)
    projects = models.ManyToManyField(
        "projects.Project",
        related_name="professors",
        blank=True,
    )

    def create_project(
        self,
        project_name,
        open_slots,
        capacity,
        meeting_schedule,
        project_description=None,
        relevant_skills=None,
    ):
        if not self.is_professor:
            raise PermissionDenied("Only professors can create projects")
        project = Project.objects.create(
            project_name=project_name,
            project_description=project_description,
            open_slots=open_slots,
            capacity=capacity,
            relevant_skills=relevant_skills,
            meeting_schedule=meeting_schedule,
        )
        self.projects.add(project)

    # def edit_project(self, project, **kwargs):

    # def delete_project(self, project):

    # def add_student_to_project(self, student):

    # def remove_student_from_project(self, student):


# This signal receiver creates a UserProfile instance when a new CustomUser is created.
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.email.endswith("@csun.edu"):
            ProfessorProfile.objects.create(user=instance)
        elif instance.email.endswith("@my.csun.edu"):
            StudentProfile.objects.create(user=instance)
