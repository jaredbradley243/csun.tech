# Generated by Django 4.1.7 on 2024-01-10 01:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0013_remove_professorprofile_rate_my_professor_link"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="is_active",
            field=models.BooleanField(default=False, verbose_name="active"),
        ),
    ]