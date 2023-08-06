from rest_framework import serializers
from .models import Project, MeetingTime


class MeetingTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingTime
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    meeting_schedule = MeetingTimeSerializer(many=True)

    class Meta:
        model = Project
        fields = "__all__"

    def create(self, validated_data):
        meeting_schedule_data = validated_data.pop("meeting_schedule")
        project = Project.objects.create(**validated_data)
        for meeting_data in meeting_schedule_data:
            MeetingTime.objects.create(project=project, **meeting_data)
        return project

    def update(self, instance, validated_data):
        meeting_schedule_data = validated_data.pop("meeting_schedule")
        instance.meeting_schedule.all().delete()  # Delete existing meeting times
        for meeting_data in meeting_schedule_data:
            MeetingTime.objects.create(project=instance, **meeting_data)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
