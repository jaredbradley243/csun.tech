from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from rest_framework import serializers
from .models import (
    CustomUser,
    StudentProfile,
    TeamLeadProfile,
    ProfessorProfile,
)
import logging
from googlesearch import search


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # fields = "__all__"
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


class StudentProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, help_text="Required")
    password = serializers.CharField(write_only=True, help_text="Required")

    class Meta:
        model = StudentProfile
        fields = "__all__"
        extra_kwargs = {
            "student_id": {"help_text": "Required"},
            "user": {"read_only": True},
        }

    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        student_id = validated_data.get("student_id")
        if email and not email.endswith("@my.csun.edu"):
            raise serializers.ValidationError(
                "This user is not a student or is not using a student email"
            )

        user = None
        try:
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
            )

            if user.email.endswith("@my.csun.edu"):
                student_profile = StudentProfile.objects.create(
                    user=user, student_id=student_id
                )
        except (ValidationError, IntegrityError) as e:
            if user:
                user.delete()
            raise serializers.ValidationError(str(e))

        return student_profile


class TeamLeadProfileSerializer(StudentProfileSerializer):
    class Meta(StudentProfileSerializer.Meta):
        model = TeamLeadProfile


class ProfessorProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, help_text="Required")
    password = serializers.CharField(write_only=True, help_text="Required")

    class Meta:
        model = ProfessorProfile
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True},
        }

    # * Included in the serializer so RMP link will resolve before API response is sent
    def set_default_RMP_link(self, professor_object):
        try:
            RMP_link = list(
                search(
                    f"{professor_object.user.first_name} "
                    + f" {professor_object.user.last_name}"
                    + " Rate My professor California State University - Northridge",
                    num_results=1,
                )
            )[0]

            professor_object.rate_my_professor_link = RMP_link
            professor_object.save()

        except Exception as e:
            logging.error(f"An error occurred while updating RMP link: {str(e)}")

    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        csun_faculty_page_link = validated_data.get("csun_faculty_page_link")
        if email and not email.endswith("@csun.edu"):
            raise serializers.ValidationError(
                "This user is not a professor or is not using a professor email"
            )

        user = None
        try:
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
            )

            if user.email.endswith("@csun.edu"):
                professor_profile = ProfessorProfile.objects.create(
                    user=user, csun_faculty_page_link=csun_faculty_page_link
                )
        except (ValidationError, IntegrityError) as e:
            if user:
                user.delete()
            raise serializers.ValidationError(str(e))

        self.set_default_RMP_link(professor_profile)

        return professor_profile


class CustomStudentProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = StudentProfile
        fields = [
            "first_name",
            "last_name",
            "email",
            "id",
            "team_lead",
            "is_volunteer",
            "student_id",
            "resume",
            "user",
            "project",
        ]


class CustomProfessorProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = ProfessorProfile
        fields = [
            "first_name",
            "last_name",
            "email",
            "id",
            "rate_my_professor_link",
            "csun_faculty_page_link",
            "bio",
            "user",
            "projects",
        ]
