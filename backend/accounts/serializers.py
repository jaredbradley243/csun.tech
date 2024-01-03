from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.db import IntegrityError, transaction
from .models import (
    CustomUser,
    StudentProfile,
    ProfessorProfile,
)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "password",
            "email",
            "first_name",
            "last_name",
            "email_confirmed",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "first_name": {"read_only": True},
            "last_name": {"read_only": True},
            "email_confirmed": {"write_only": True},
        }


# #! Student profile always created with team lead false, even if specified otherwise
class StudentProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, help_text="Required")
    password = serializers.CharField(write_only=True, help_text="Required")
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)

    class Meta:
        model = StudentProfile
        fields = "__all__"
        extra_kwargs = {
            "student_id": {"help_text": "Required"},
            "user": {"read_only": True},
        }


# * This serializer is nested in the ProjectDetailSerializer in /projects/serializers.py
# * to show detailed professor information in the project detail
class ProfessorProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = ProfessorProfile
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True},
        }


# * This serializer is nested in the ProjectListSerializer in /projects/serializers.py
# * to show basic professor information in the project list and dashboard
class ProfessorNameSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)

    class Meta:
        model = ProfessorProfile
        fields = ["first_name", "last_name", "id"]


# * Used for Professor Dashboard
class ProfessorDashboardStudentSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = StudentProfile
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "team_lead",
            "is_volunteer",
            "student_id",
            "resume",
            "user",
            "project",
        ]


# class UserProfileStudentSerializer(serializers.ModelSerializer):
#     team_lead = serializers.BooleanField(
#         source="studentprofile.team_lead", read_only=True
#     )
#     volunteer = serializers.BooleanField(
#         source="studentprofile.is_volunteer", read_only=True
#     )
#     student_id = serializers.CharField(
#         source="studentprofile.student_id", read_only=True
#     )
#     resume = serializers.FileField(source="studentprofile.resume")
#     project = serializers.CharField(source="studentprofile.project", read_only=True)

#     class Meta:
#         model = CustomUser
#         fields = [
#             "id",
#             "first_name",
#             "last_name",
#             "email",
#             "student_id",
#             "resume",
#             "team_lead",
#             "volunteer",
#             "project",
#         ]
#         extra_kwargs = {
#             "id": {"read_only": True},
#             "first_name": {"read_only": True},
#             "last_name": {"read_only": True},
#             "email": {"read_only": True},
#             # team_lead: readonly specified in serializer
#             # volunteer: readonly specified in serializer
#             # student_id: readonly specified in serializer
#             # Resume can be updated
#             # project: readonly specified in serializer
#         }


class UserProfileStudentSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source="user.id", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    project = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            "user_id",
            "id",
            "first_name",
            "last_name",
            "email",
            "student_id",
            "resume",
            "team_lead",
            "is_volunteer",
            "project",
        ]
        extra_kwargs = {
            # user_id: readonly specified in serializer
            "id": {"read_only": True},
            # first_name: readonly specified in serializer
            # last_name: readonly specified in serializer
            # email: readonly specified in serializer
            "student_id": {"required": False},
            # Resume can be updated
            "team_lead": {"read_only": True},
            "is_volunteer": {"read_only": True},
            # project: readonly specified in serializer
        }

    def update(self, instance, validated_data):
        student_profile = instance.studentprofile
        student_profile.student_id = validated_data.get(
            "student_id", student_profile.student_id
        )
        student_profile.resume = validated_data.get("resume", student_profile.resume)
        student_profile.save()
        return super().update(instance, validated_data)


class UserProfileProfessorSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source="user.id", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    projects = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = ProfessorProfile
        fields = [
            "user_id",
            "id",
            "first_name",
            "last_name",
            "email",
            "bio",
            "csun_faculty_page_link",
            "projects",
        ]
        extra_kwargs = {
            # user_id: readonly specified in serializer
            "id": {"read_only": True},
            # first_name: readonly specified in serializer
            # last_name: readonly specified in serializer
            # email: readonly specified in serializer
            # Bio can be updated
            "csun_faculty_page_link": {"read_only": True},
            # project: readonly specified in serializer
        }

    def update(self, instance, validated_data):
        professor_profile = instance.professorprofile
        professor_profile.bio = validated_data.get("bio", professor_profile.bio)
        professor_profile.save()
        return super().update(instance, validated_data)
