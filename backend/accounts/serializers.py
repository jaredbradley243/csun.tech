from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from rest_framework import serializers
from .models import (
    CustomUser,
    StudentProfile,
    TeamLeadProfile,
    ProfessorProfile,
)
import ratemyprofessor
import logging


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

    def fetch_and_update_rmp_data(self, professor_object):
        try:
            school = ratemyprofessor.get_school_by_name(
                "California State University Northridge"
            )
            rmp_professor = ratemyprofessor.get_professor_by_school_and_name(
                school,
                f"{professor_object.user.first_name} {professor_object.user.last_name}",
            )
            if rmp_professor is None:
                raise ValidationError("Professor not found on RMP")
            prof_rating = rmp_professor.rating
            if not prof_rating:
                raise ValidationError("Professor has no rating or rating not found")
            prof_would_take_again = rmp_professor.would_take_again
            if not prof_would_take_again:
                raise ValidationError(
                    "Professor has no would take again rating or rating not found"
                )
            prof_difficulty = rmp_professor.difficulty
            if not prof_difficulty:
                raise ValidationError(
                    "Professor has no difficulty rating or difficulty rating not found"
                )
            changes_made = False

            if prof_rating is not None:
                professor_object.rate_my_professor_rating = prof_rating
                changes_made = True
            if prof_would_take_again is not None:
                professor_object.rate_my_professor_would_take_again = (
                    prof_would_take_again
                )
                changes_made = True
            if prof_difficulty is not None:
                professor_object.rate_my_professor_difficulty = prof_difficulty
                changes_made = True

            if changes_made:
                professor_object.save()

        except Exception as e:
            logging.error(
                f"An error occurred while updating RMP data: {str(e)}"
            )  # For debugging purposes

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
        self.fetch_and_update_rmp_data(professor_profile)

        return professor_profile


#! Added This
class CustomStudentProfileSerializer(serializers.ModelSerializer):
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


#! Added This
class CustomProfessorProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = ProfessorProfile
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "rate_my_professor_rating",
            "rate_my_professor_difficulty",
            "rate_my_professor_would_take_again",
            "csun_faculty_page_link",
            "bio",
            "user",
            "projects",
            # add other fields as needed
        ]
