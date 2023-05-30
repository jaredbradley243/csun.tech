from django.db import models
from django.core.validators import MaxValueValidator


class Project(models.Model):
    project_name = models.CharField(null=False, max_length=100, unique=True)
    project_description = models.CharField(null=True, blank=True, max_length=500)
    open_slots = models.IntegerField(
        null=True, blank=True, validators=[MaxValueValidator(2)]
    )
    capacity = models.IntegerField(
        null=True, blank=True, validators=[MaxValueValidator(2)]
    )
    relevant_skills = models.CharField(null=True, blank=True, max_length=500)
    meeting_schedule = models.ManyToManyField("MeetingTime")

    def __str__(self):
        return self.project_name


class DayofWeek:
    MONDAY = "MON"
    TUESDAY = "TUE"
    WEDNESDAY = "WED"
    THURSDAY = "THU"
    FRIDAY = "FRI"
    SATURDAY = "SAT"
    SUNDAY = "SUN"
    CHOICES = [
        (MONDAY, "M"),
        (TUESDAY, "T"),
        (WEDNESDAY, "W"),
        (THURSDAY, "Th"),
        (FRIDAY, "F"),
        (SATURDAY, "S"),
        (SUNDAY, "Su"),
    ]


class MeetingTime(models.Model):
    day_of_week = models.CharField(max_length=3, choices=DayofWeek.CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.get_day_of_week_display()} {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
