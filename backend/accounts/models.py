from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
import uuid
from django.core.validators import (
    FileExtensionValidator,
    MinLengthValidator,
    MaxLengthValidator,
)
from django.core.exceptions import ValidationError

from rest_framework.exceptions import PermissionDenied
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
            raise ValidationError("User must us a CSUN email address")

        """" Get Name From Email """
        full_name = email.split("@")[0]
        if not full_name:
            raise ValidationError("Email must contain @")

        name_parts = full_name.split(".")
        if len(name_parts) < 2:
            raise ValidationError(
                "Email should have first name and last name separated by a period"
            )

        # * Get First Name From name_parts
        first_name = name_parts[0]
        if not first_name:
            raise ValidationError("First name must be present in email")
        first_name = first_name.replace("-", " ").capitalize()
        # if not first_name:
        #     raise ValidationError("First name must be present in email")

        # * Get Last Name From name_parts
        last_name = name_parts[1]
        if not last_name:
            raise ValidationError("Last name must be present in email")

        last_name = last_name.replace("-", " ").capitalize()

        user = self.model(
            email=email, first_name=first_name, last_name=last_name, **extra_fields
        )

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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, blank=False)
    username = models.CharField(max_length=150, unique=True, default="")
    first_name = models.CharField(max_length=30, blank=True, verbose_name="first name")
    last_name = models.CharField(max_length=30, blank=True, verbose_name="last name")
    is_staff = models.BooleanField(default=False, verbose_name="staff")
    email_confirmed = models.BooleanField(default=False, verbose_name="email confirmed")
    is_active = models.BooleanField(default=False, verbose_name="active")

    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    # For createsuperuser commands
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

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

    @property
    def is_student(self):
        return self.email.endswith("@my.csun.edu")

    @property
    def is_team_lead(self):
        if hasattr(self, "studentprofile"):
            return self.studentprofile.team_lead

    @property
    def is_professor(self):
        return self.email.endswith("@csun.edu")

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)


class StudentProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

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

    def join_project(self, project):
        if self.project:
            raise ValidationError("Student is already enrolled in a project")
        project.add_student(self)

    def leave_project(self):
        if not self.project:
            raise ValidationError("Student is not enrolled in a project")
        self.project.remove_student(self)


class TeamLeadProfile(StudentProfile):
    class Meta:
        proxy = True

    def add_student_to_project(self, student):
        if not self.project:
            raise ValidationError("Team lead is not enrolled in a project")
        self.project.add_student(student, self)

    def remove_student_from_project(self, student):
        if not self.project:
            raise ValidationError("Team lead is not enrolled in a project")
        self.project.remove_student(student, self)


class ProfessorProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    csun_faculty_page_link = models.URLField(
        blank=True,
        null=True,
    )
    projects = models.ManyToManyField(
        "projects.Project",
        related_name="professors",
        blank=True,
    )
    bio = models.TextField(blank=True)

    def get_projects(self):
        return self.projects.all()

    def create_project(
        self,
        project_name,
        open_slots,
        capacity,
        # meeting_schedule=None,
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
            # meeting_schedule=meeting_schedule,
        )
        self.projects.add(project)

    # TODO: Modify Function to error check
    def leave_project(self, project):
        self.projects.remove(project)

    # TODO: Modify Function to error check
    def edit_project(self, project, **kwargs):
        if project in self.projects.all():
            for attr, value in kwargs.items():
                if hasattr(project, attr):
                    setattr(project, attr, value)
                else:
                    raise ValidationError(f"Project has no attribute {attr}")
            project.save()
        else:
            raise ValidationError("Professor is not associated with this project")

    def delete_project(self, project):
        if project in self.projects.all():
            project.delete()
        else:
            raise ValidationError("Professor is not associated with this project")

    def add_student_to_project(self, student, project):
        if project not in self.get_projects():
            raise ValidationError("Project not found in professor's projects")

        if student.project:
            raise ValidationError("Selected student is already enrolled in a project")

        project.add_student(student, self)

    def remove_student_from_project(self, student, project):
        if project not in self.get_projects():
            raise ValidationError("Project not found in professor's projects")

        if student.project != project:
            raise ValidationError(
                "Selected student is not enrolled in the selected project"
            )

        project.remove_student(student, self)


@receiver(post_save, sender=ProfessorProfile)
def set_default_csun_faculty_page_link(sender, instance, **kwargs):
    if not instance.csun_faculty_page_link:
        instance.csun_faculty_page_link = (
            "https://academics.csun.edu/faculty/"
            + f"{instance.user.first_name.lower()}"
            + f".{instance.user.last_name.lower()}/"
        )
        instance.save()
