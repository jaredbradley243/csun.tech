from email.message import EmailMessage
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectListSerializer, ProjectDetailSerializer
from django.shortcuts import get_object_or_404
from accounts.models import (
    CustomUser,
    StudentProfile,
    ProfessorProfile,
    TeamLeadProfile,
)


class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    # serializer_class = ProjectListSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        return ProjectDetailSerializer

    # TODO: Handle Team lead and professors adding students to project
    @action(detail=True, methods=["post"], url_path="students")
    def join_project(self, request, pk=None):
        # TODO: Handle Students Joining Project
        user_id = request.data.get("user_id")

        if not user_id or not isinstance(user_id, str):
            return Response(
                {"error": "Valid user ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_instance = get_object_or_404(CustomUser, pk=user_id)
        project = self.get_object()

        if user_instance.is_student:
            user_instance.studentprofile.join_project(project)

        # 3. Use student object to call "join_project(self, project)" on student profile
        # 4. Return appropriate response

        # TODO: Handle professor inv another prof to join Project
        # pass

        # try:
        #     student_profile = self.get_object()
        # except Http404:
        #     return Response(
        #         "Student profile not found", status=status.HTTP_404_NOT_FOUND
        #     )
        # project_id = request.data.get("project")
        # if project_id is None:
        #     return Response("Missing project_id", status=status.HTTP_400_BAD_REQUEST)
        # try:
        #     project_id = int(project_id)
        #     if project_id <= 0:
        #         raise ValueError()
        # except ValueError:
        #     return Response("Invalid project_id", status=status.HTTP_400_BAD_REQUEST)
        # try:
        #     project = Project.objects.get(pk=project_id)
        # except ObjectDoesNotExist:
        #     return Response("Project does not exist", status=status.HTTP_404_NOT_FOUND)
        # try:
        #     student_profile.join_project(project)
        # except ValidationError as e:
        #     return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        # serializer = StudentProfileSerializer(student_profile)
        return Response(status=status.HTTP_200_OK)

    # TODO: Handle Team lead and professors removing students from project
    # TODO: Handle professor removing another prof from Project
    @action(detail=True, methods=["post"], url_path="students")
    def leave_project(self, request, pk=None):
        # TODO: Handle Students leaving Project

        # TODO: Handle professor leaving Project
        pass
