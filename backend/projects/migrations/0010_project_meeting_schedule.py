# Generated by Django 4.1.7 on 2023-06-09 23:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0009_remove_project_meeting_schedule"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="meeting_schedule",
            field=models.ManyToManyField(to="projects.meetingtime"),
        ),
    ]
