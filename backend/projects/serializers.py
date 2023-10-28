from rest_framework import serializers
from .models import Project
from accounts.serializers import (
    ProfessorProfileSerializer,
    CustomUserSerializer,
    CustomProfessorProfileSerializer,
)

from datetime import datetime


# TODO - Add email validations
# 1) Create verification token
# 2) Send email to user with verification token
class ProjectSerializer(serializers.ModelSerializer):
    professors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Project
        fields = "__all__"
        extra_kwargs = {
            "project_name": {"help_text": "Required"},
            "open_slots": {"help_text": "Required"},
            "capacity": {"help_text": "Required"},
        }

    def validate_meeting_schedule(self, meeting_schedule_list):
        if meeting_schedule_list is None or len(meeting_schedule_list) == 0:
            return []

        valid_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        if not isinstance(meeting_schedule_list, list):
            raise serializers.ValidationError("meeting_schedule should be a list")

        for meeting_dict in meeting_schedule_list:
            if not isinstance(meeting_dict, dict):
                raise serializers.ValidationError(
                    "Each item in meeting_schedule should be a dictionary"
                )

            required_keys = ["day", "start_time", "end_time"]
            for key in required_keys:
                if key not in meeting_dict:
                    raise serializers.ValidationError(
                        f"{key} is required in each meeting dictionary"
                    )

            time_format = "%H:%M"  # 24-hour format
            for time_key in ["start_time", "end_time"]:
                try:
                    time_obj = datetime.strptime(meeting_dict[time_key], time_format)
                    meeting_dict[time_key] = datetime.strftime(time_obj, time_format)
                except ValueError:
                    raise serializers.ValidationError(
                        f"{time_key} should be in {time_format} format"
                    )

            normalized_day = meeting_dict["day"].title()
            if normalized_day not in valid_days:
                raise serializers.ValidationError(
                    "day must be one of the valid days: {}".format(
                        ", ".join(valid_days)
                    )
                )
            meeting_dict["day"] = normalized_day

        return meeting_schedule_list

    def validate(self, data):
        open_slots = data.get("open_slots", None)
        capacity = data.get("capacity", None)

        if open_slots is not None and capacity is not None:
            if open_slots > capacity:
                raise serializers.ValidationError(
                    "open_slots should not exceed capacity"
                )
        return data

    def create(self, validated_data):
        project = Project.objects.create(**validated_data)
        return project

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


#! Added This
class CustomProjectSerializer(serializers.ModelSerializer):
    professors = CustomProfessorProfileSerializer(many=True, read_only=True)
    project_id = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = Project
        # fields = "__all__"
        fields = [
            "project_id",
            "project_name",
            "project_description",
            "open_slots",
            "capacity",
            "relevant_skills",
            "meeting_schedule",
            "professors",
        ]
