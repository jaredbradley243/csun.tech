from django.db import models
from django.core.validators import MaxValueValidator
from django.db.models import JSONField
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.core.exceptions import ValidationError
from datetime import datetime


# TODO: Add validation to ensure that open_slots can never exceed capacity
class Project(models.Model):
    project_name = models.CharField(null=False, max_length=100, unique=True)
    project_description = models.CharField(null=True, blank=True, max_length=500)
    open_slots = models.IntegerField(validators=[MaxValueValidator(99)])
    capacity = models.IntegerField(validators=[MaxValueValidator(99)])
    relevant_skills = models.CharField(null=True, blank=True, max_length=500)
    meeting_schedule = JSONField(null=True, blank=True)

    def __str__(self):
        return self.project_name

    def add_student(self, student, authority=None):
        if authority and not (authority.is_team_lead or authority.is_professor):
            raise PermissionDenied("Only Team Leads or Professors can add students")
        if authority and authority.is_team_lead and authority.project != self:
            raise PermissionDenied("Team Lead can only add students to their project")
        if (
            authority
            and authority.is_professor
            and self not in authority.get_projects()
        ):
            raise PermissionDenied(
                "Professor can only add students to their own projects"
            )
        if student.project:
            raise ValidationError("Selected student is already enrolled in a project")
        if self.open_slots <= 0:
            raise ValidationError("Project is full")
        self.open_slots -= 1
        self.save()
        student.project = self
        student.save()

    def remove_student(self, student, authority=None):
        if authority and not (authority.is_team_lead or authority.is_professor):
            raise PermissionDenied("Only Team Leads or Professors can remove students")
        if not student.project:
            raise ValidationError("Selected student is not enrolled in a project")
        if student.project != self:
            raise ValidationError("Student is not enrolled in this project")
        if authority and (authority.is_team_lead and authority.project != self):
            raise PermissionDenied(
                "Team Lead can only remove students from their project"
            )
        student.project = None
        student.save()
        self.open_slots += 1
        self.save()

    def add_professor(self, professor):
        professor.projects.add(self)

    def remove_professor(self, professor):
        professor.projects.remove(self)

    def save(self, *args, **kwargs):
        self.validate_open_slots()
        super().save(*args, **kwargs)

    def validate_open_slots(self):
        if self.open_slots > self.capacity:
            raise ValidationError("Open slots cannot exceed capacity")
