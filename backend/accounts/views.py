from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from email.message import EmailMessage
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from rest_framework.exceptions import MethodNotAllowed

from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CustomUser, StudentProfile, ProfessorProfile, TeamLeadProfile
from projects.models import Project
from .serializers import (
    CustomUserSerializer,
    StudentProfileSerializer,
    ProfessorProfileSerializer,
    CustomStudentProfileSerializer,
    TeamLeadProfileSerializer,
)
from django.shortcuts import get_object_or_404
from projects.serializers import CustomProjectSerializer


# TODO - Protect endpoints from non-authenticated and non-authorized users
# Todo - For example, only authenticated users, and specifically students can join projects


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ["get", "put", "patch", "delete", "head", "options", "trace"]

    def update(self, request, *args, **kwargs):
        if "first_name" in request.data or "last_name" in request.data:
            return Response(
                {
                    "First and last name are determined by user's email"
                    + " address and cannot be updated directly"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        request_data_id = request.data.get("id", None)
        request_data_user = request.data.get("user", None)
        if request_data_id and request_data_id != str(instance.id):
            return Response(
                "User IDs cannot be changed", status=status.HTTP_400_BAD_REQUEST
            )
        if request_data_user and request_data_user != str(instance.user.id):
            return Response(
                "User IDs cannot be changed", status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def join_project(self, request, pk=None):
        try:
            student_profile = self.get_object()
        except Http404:
            return Response(
                "Student profile not found", status=status.HTTP_404_NOT_FOUND
            )
        project_id = request.data.get("project")
        if project_id is None:
            return Response("Missing project_id", status=status.HTTP_400_BAD_REQUEST)
        try:
            project_id = int(project_id)
            if project_id <= 0:
                raise ValueError()
        except ValueError:
            return Response("Invalid project_id", status=status.HTTP_400_BAD_REQUEST)
        try:
            project = Project.objects.get(pk=project_id)
        except ObjectDoesNotExist:
            return Response("Project does not exist", status=status.HTTP_404_NOT_FOUND)
        try:
            student_profile.join_project(project)
        except ValidationError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        serializer = StudentProfileSerializer(student_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def leave_project(self, request, pk=None):
        try:
            student_profile = self.get_object()
        except Http404:
            return Response(
                "Student profile not found", status=status.HTTP_404_NOT_FOUND
            )
        try:
            student_profile.leave_project()
        except ValidationError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        serializer = StudentProfileSerializer(student_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeamLeadProfileViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = TeamLeadProfile.objects.filter(team_lead=True)
    serializer_class = TeamLeadProfileSerializer

    # TODO - Add error handling
    @action(detail=True, methods=["post"])
    def add_student_to_project(self, request, pk=None):
        teamleadprofile_id = pk
        studentprofile_id = request.data.get("studentprofile_id")
        studentprofile = get_object_or_404(StudentProfile, id=studentprofile_id)
        teamleadprofile = get_object_or_404(TeamLeadProfile, id=teamleadprofile_id)

        teamleadprofile.add_student_to_project(studentprofile)
        # your logic to add a student to a project
        return Response({"status": "student added to project"})

    # TODO - Add error handling
    @action(detail=True, methods=["post"])
    def remove_student_from_project(self, request, pk=None):
        teamleadprofile_id = pk
        studentprofile_id = request.data.get("studentprofile_id")
        studentprofile = get_object_or_404(StudentProfile, id=studentprofile_id)
        teamleadprofile = get_object_or_404(TeamLeadProfile, id=teamleadprofile_id)

        teamleadprofile.remove_student_from_project(studentprofile)
        return Response({"status": "student removed from project"})


class ProfessorProfileViewSet(viewsets.ModelViewSet):
    queryset = ProfessorProfile.objects.all()
    serializer_class = ProfessorProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        request_data_id = request.data.get("id", None)
        request_data_user = request.data.get("user", None)
        if request_data_id and request_data_id != str(instance.id):
            return Response(
                "User IDs cannot be changed", status=status.HTTP_400_BAD_REQUEST
            )
        if request_data_user and request_data_user != str(instance.user.id):
            return Response(
                "User IDs cannot be changed", status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfessorDashboardViewSet(viewsets.ViewSet):
    def list(self, request, professor_id=None):
        professor = get_object_or_404(ProfessorProfile, id=professor_id)
        projects = professor.projects.all()
        students = StudentProfile.objects.filter(project__in=projects).select_related(
            "user"
        )

        students_data = CustomStudentProfileSerializer(students, many=True).data
        projects_data = CustomProjectSerializer(projects, many=True).data

        return Response(
            {
                "students": students_data,
                "projects": projects_data,
            }
        )


def index(request):
    return HttpResponse("Hello, world. You're at the index.")


def register(request):
    return HttpResponse("Hello, world. You're at the register page.")
