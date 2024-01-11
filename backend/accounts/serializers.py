from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.db import IntegrityError, transaction
from .models import CustomUser, StudentProfile, ProfessorProfile, CustomUserManager
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    student_id = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = CustomUser
        fields = "__all__"

    @transaction.atomic
    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        if email.endswith("@my.csun.edu"):
            student_id = validated_data.get("student_id")
            if not student_id:
                raise serializers.ValidationError(
                    "User is a student, but no student ID was given"
                )
        try:
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
            )

            if user.email.endswith("@my.csun.edu"):
                StudentProfile.objects.create(user=user, student_id=student_id)

            elif user.email.endswith("@csun.edu"):
                ProfessorProfile.objects.create(user=user)

        except (ValidationError, IntegrityError) as e:
            raise serializers.ValidationError(str(e))

        return user


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        custom_user_instance = self.user
        data.update(
            {
                "id": custom_user_instance.id,
                "first_name": custom_user_instance.first_name,
                "last_name": custom_user_instance.last_name,
                "email": custom_user_instance.email,
            }
        )
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
        # TODO: Remove fields above and uncomment fields/extra kw below
        # fields = [
        #     "id",
        #     "password",
        #     "email",
        #     "first_name",
        #     "last_name",
        #     "email_confirmed",
        # ]
        # extra_kwargs = {
        #     "password": {"write_only": True},
        #     "first_name": {"read_only": True},
        #     "last_name": {"read_only": True},
        #     "email_confirmed": {"write_only": True},
        # }


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
