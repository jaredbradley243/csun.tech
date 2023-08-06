from email.message import EmailMessage
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CustomUser, UserProfile, StudentProfile
from .serializers import (
    CustomUserSerializer,
    UserProfileSerializer,
    StudentProfileSerializer,
)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer

    @action(detail=True, methods=["post"])
    def join_project(self, request, pk=None):
        student_profile = self.get_object()
        project_id = request.data.get("project_id")
        project = Project.objects.get(pk=project_id)

        try:
            student_profile.join_project(project)
            serializer = StudentProfileSerializer(student_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


def index(request):
    return HttpResponse("Hello, world. You're at the index.")


def register(request):
    return HttpResponse("Hello, world. You're at the register page.")
