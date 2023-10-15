from rest_framework import serializers
from .models import (
    CustomUser,
    UserProfile,
    StudentProfile,
    TeamLeadProfile,
    ProfessorProfile,
)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = UserProfile
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        groups_data = user_data.pop("groups", None)
        user_data.pop("user_permissions", None)
        user = CustomUser.objects.create(**user_data)
        user.groups.set(groups_data)  # Set the many-to-many relationship
        user_profile = UserProfile.objects.create(user=user, **validated_data)
        return user_profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        user_instance = instance.user

        user_instance.first_name = user_data.get("first_name", user_instance.first_name)
        user_instance.last_name = user_data.get("last_name", user_instance.last_name)
        user_instance.email = user_data.get("email", user_instance.email)
        user_instance.username = user_data.get("username", user_instance.username)
        user_instance.is_staff = user_data.get("is_staff", user_instance.is_staff)
        user_instance.email_confirmed = user_data.get(
            "email_confirmed", user_instance.email_confirmed
        )
        user_instance.is_active = user_data.get("is_active", user_instance.is_active)
        user_instance.set_password(user_data.get("password", user_instance.password))

        instance.user.save()

        # Update UserProfile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class StudentProfileSerializer(UserProfileSerializer):
    class Meta(UserProfileSerializer.Meta):
        model = StudentProfile

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        groups_data = user_data.pop("groups", None)
        user_data.pop("user_permissions", None)
        user = CustomUser.objects.create(**user_data)
        user.groups.set(groups_data)

        if user.email.endswith("@csun.edu"):
            user.delete()
            raise serializers.ValidationError("This user is not a student")
        elif user.email.endswith("@my.csun.edu"):
            user_profile = StudentProfile.objects.create(user=user, **validated_data)
        else:
            user.delete()
            raise serializers.ValidationError("Email address must be CSUN email")
        return user_profile


class TeamLeadProfileSerializer(StudentProfileSerializer):
    class Meta(StudentProfileSerializer.Meta):
        model = TeamLeadProfile


# TODO - Finish Professor Profile
class ProfessorProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = ProfessorProfile
        fields = "__all__"  # or specify the fields you want to include
