# Generated by Django 4.1.7 on 2023-10-24 04:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0006_alter_professorprofile_csun_faculty_page_link_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="professorprofile",
            name="rate_my_professor_link",
        ),
        migrations.AddField(
            model_name="professorprofile",
            name="rate_my_professor_difficulty",
            field=models.IntegerField(blank=True, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="professorprofile",
            name="rate_my_professor_rating",
            field=models.IntegerField(blank=True, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="professorprofile",
            name="rate_my_professor_would_take_again",
            field=models.IntegerField(blank=True, default=0),
            preserve_default=False,
        ),
    ]
