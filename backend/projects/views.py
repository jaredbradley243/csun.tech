from uuid import UUID
from email.message import EmailMessage
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db import transaction

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
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
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        return ProjectDetailSerializer

    def create(self, request, *args, **kwargs):
        if not request.user.is_professor:
            return Response(
                {"error": "Unauthorized action. Only professors can create projects"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not request.user.is_professor:
            return Response(
                {"error": "Unauthorized action. Only professors can update projects"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not request.user.is_professor:
            return Response(
                {"error": "Unauthorized action. Only professors can update projects"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_professor:
            return Response(
                {"error": "Unauthorized action. Only professors can delete projects"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().create(request, *args, **kwargs)

    # TODO: Handle student already being enrolled in a project
    # TODO: Handle Team lead and professors adding students to project
    # TODO: Handle professor inv another prof to join Project
    @action(detail=True, methods=["post"], url_path="students")
    @transaction.atomic
    def join_project(self, request, pk=None):
        user_id = request.data.get("user_id")

        if not user_id:
            return Response(
                {"error": "Valid user ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            UUID(user_id, version=4)
        except ValueError:
            return Response(
                {"error": "Invalid user ID format."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_instance = get_object_or_404(CustomUser, pk=user_id)
        project_instance = self.get_object()

        if user_instance == request.user:
            if user_instance.studentprofile.project:
                user_instance.studentprofile.leave_project()
            user_instance.studentprofile.join_project(project_instance)
            project_instance.refresh_from_db()
        else:
            return Response(
                {
                    "error": "Unauthorized action. You cannot add another user to a project."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        project_serializer_instance = ProjectDetailSerializer(project_instance)
        return Response(
            {
                "message": "You have successfully joined the project.",
                "open_slots": project_serializer_instance.data["open_slots"],
            },
            status=status.HTTP_200_OK,
        )

    # TODO: Handle Team lead and professors removing students from project
    # TODO: Handle professor removing another prof from Project
    # TODO: Handle professor leaving Project
    @action(detail=False, methods=["delete"], url_path="students/<str:user_id>/")
    @transaction.atomic
    def leave_project(self, request, user_id):
        if not user_id:
            return Response(
                {"error": "Valid user ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            UUID(user_id, version=4)
        except ValueError:
            return Response(
                {"error": "Invalid user ID format."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_instance = get_object_or_404(CustomUser, pk=user_id)

        project_instance = user_instance.studentprofile.project

        if not project_instance:
            return Response(
                {"error": "User is not associated with any project."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user_instance == request.user:
            user_instance.studentprofile.leave_project()
            project_instance.refresh_from_db()
        else:
            return Response(
                {
                    "error": "Unauthorized action. You cannot remove another user from a project."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        project_serializer_instance = ProjectDetailSerializer(project_instance)
        return Response(
            {
                "message": "You have successfully left the project.",
                "open_slots": project_serializer_instance.data["open_slots"],
            },
            status=status.HTTP_200_OK,
        )
