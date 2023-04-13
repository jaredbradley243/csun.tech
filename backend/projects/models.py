from django.db import models
from django.contrib.auth import (
    get_user_model,
)  # TODO: import UserProfile when issue #1 is merged


class DayofWeek(models.Model):
    MONDAY = "MON", "Monday"
    TUESDAY = "TUE", "Tuesday"
    WEDNESDAY = "WED", "Wednesday"
    THURSDAY = "THU", "Thursday"
    FRIDAY = "FRI", "Friday"
    SATURDAY = "SAT", "Saturday"
    SUNDAY = "SUN", "Sunday"

    choices = [
        MONDAY,
        TUESDAY,
        WEDNESDAY,
        THURSDAY,
        FRIDAY,
        SATURDAY,
        SUNDAY,
    ]


class MeetingTime(models.Model):
    day_of_week = models.CharField(max_length=3, choices=DayofWeek.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.day_of_week} {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"


# SeniorProject model
class ProjectProfile(models.Model):
    project_name = models.CharField(max_length=100)
    professor_name = models.CharField(max_length=100)
    open_spots = models.PositiveIntegerField()
    total_spots = models.PositiveIntegerField()
    project_description = models.TextField()
    neccesary_skills = models.TextField()
    meeting_times = models.ManyToManyField(MeetingTime, blank=True)
    student_list = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="project_profiles",
        null=True,
        blank=True,
    )  # TODO: reference UserProfile.first_name & UserProfile.last_name when issue #1 is merged

    def __str__(self):
        return self.project_name
