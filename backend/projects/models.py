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

    def save(self, *args, **kwargs):
        self.validate_meeting_schedule()
        self.validate_open_slots()
        super().save(*args, **kwargs)

    def validate_meeting_schedule(self):
        if self.meeting_schedule is not None:
            valid_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            if not isinstance(self.meeting_schedule, list):
                raise ValidationError("meeting_schedule should be a list")

            for meeting_dict in self.meeting_schedule:
                if not isinstance(meeting_dict, dict):
                    raise ValidationError(
                        "Each item in meeting_schedule should be a dictionary"
                    )

                required_keys = ["day", "start_time", "end_time"]
                for key in required_keys:
                    if key not in meeting_dict:
                        raise ValidationError(
                            f"{key} is required in each meeting dictionary"
                        )

                time_format = "%H:%M"  # 24-hour format
                for time_key in ["start_time", "end_time"]:
                    try:
                        time_obj = datetime.strptime(
                            meeting_dict[time_key], time_format
                        )
                        meeting_dict[time_key] = datetime.strftime(
                            time_obj, time_format
                        )
                    except ValueError:
                        raise ValidationError(
                            f"{time_key} should be in {time_format} format"
                        )

                normalized_day = meeting_dict["day"].title()
                if normalized_day not in valid_days:
                    raise ValidationError(
                        "day must be one of the valid days: {}".format(
                            ", ".join(valid_days)
                        )
                    )
                meeting_dict["day"] = normalized_day

    def validate_open_slots(self):
        if self.open_slots > self.capacity:
            raise ValidationError("Open slots cannot exceed capacity")
