from django.db import models
from django.core.validators import MaxValueValidator
from rest_framework.exceptions import ValidationError, PermissionDenied


class Project(models.Model):
    project_name = models.CharField(null=False, max_length=100, unique=True)
    project_description = models.CharField(null=True, blank=True, max_length=500)
    open_slots = models.IntegerField(validators=[MaxValueValidator(2)])
    capacity = models.IntegerField(validators=[MaxValueValidator(2)])
    relevant_skills = models.CharField(null=True, blank=True, max_length=500)
    meeting_schedule = models.ManyToManyField("MeetingTime")

    def __str__(self):
        return self.project_name

    def add_student(self, student, authority=None):
        if authority and not (authority.is_team_lead or authority.is_professor):
            raise PermissionDenied("Only Team Leads or Professors can add students")
        if authority and authority.is_team_lead and authority.project != self:
            raise PermissionDenied("Team Lead can only add students to their project")
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


class DayofWeek(models.TextChoices):
    MONDAY = "MON"
    TUESDAY = "TUE"
    WEDNESDAY = "WED"
    THURSDAY = "THU"
    FRIDAY = "FRI"
    SATURDAY = "SAT"
    SUNDAY = "SUN"


class MeetingTime(models.Model):
    day_of_week = models.CharField(max_length=3, choices=DayofWeek.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.get_day_of_week_display()} {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
