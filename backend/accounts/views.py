from uuid import UUID
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import datetime

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
from .models import CustomUser, StudentProfile, ProfessorProfile
from projects.models import Project
from django.core.mail import send_mail


from .serializers import (
    CustomUserSerializer,
    # StudentProfileSerializer,
    ProfessorProfileSerializer,
    ProfessorDashboardStudentSerializer,
    ProfessorNameSerializer,
    UserProfileStudentSerializer,
    UserProfileProfessorSerializer,
    RegistrationSerializer,
    LoginSerializer,
)

from projects.serializers import (
    ProjectDetailSerializer,
    ProjectListSerializer,
    ProfessorDashboardProjectSerializer,
)
from django.shortcuts import get_object_or_404
from django.db import transaction, IntegrityError
from csuntech.settings import SECRET_KEY
from django.template.loader import render_to_string
from rest_framework_simplejwt.views import TokenObtainPairView


class RegistrationViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer
    http_method_names = ["post"]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            # * Serialize Username, Password, Student_ID.
            # * Create Custom User and Prof/student profile
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user_instance = serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # * Generate an email confirmation token
            user_id = str(user_instance.id)
            expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=1)
            payload = {"user_id": user_id, "exp": expiration_time}
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            # * Send email with link to email verification endpoint with token in URI
            send_mail(
                "Please Verify Your Email",
                "Please confirm your email address by following the link \n"
                + f"http://localhost:8000/emailverification/{token}",
                "CSUN Senior Design <noreply@seniordesignproject.com>",
                [f"{user_instance.email}"],
                html_message=render_to_string(
                    "accounts/email_verification.html", {"token": token}
                ),
                fail_silently=False,
            )
        except Exception as error:
            return Response(str(error), status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginViewSet(TokenObtainPairView):
    serializer_class = LoginSerializer
    http_method_names = ["post"]


class EmailVerificationViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @transaction.atomic
    @action(detail=False, methods=["get"])
    def verify(self, request, *args, **kwargs):
        token = kwargs.get("token", None)

        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")
                user_id = payload["user_id"]
                user_instance = get_object_or_404(CustomUser, pk=user_id)
                user_instance.email_confirmed = True
                user_instance.is_active = True
                user_instance.save()
                return Response(
                    "Email verified successfully. User may login.",
                    status=status.HTTP_200_OK,
                )
            except jwt.ExpiredSignatureError:
                return Response(
                    "TokenExpiredError",
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            except jwt.DecodeError as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                "No verification token provided.", status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["get"])
    def resend(self, request, *args, **kwargs):
        try:
            user_instance = self.get_object()
            # * Generate an email confirmation token
            user_id = str(user_instance.id)
            expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=1)
            payload = {"user_id": user_id, "exp": expiration_time}
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            # * Send email with link to email verification endpoint with token in URI
            send_mail(
                "Please Verify Your Email",
                "Please confirm your email address by following the link \n"
                + f"http://localhost:8000/emailverification/{token}",
                "CSUN Senior Design <noreply@seniordesignproject.com>",
                [f"{user_instance.email}"],
                html_message=render_to_string(
                    "accounts/email_verification.html", {"token": token}
                ),
                fail_silently=False,
            )
        except:
            return Response(
                "Email send unsuccessful", status=status.HTTP_400_BAD_REQUEST
            )
        return Response("Email sent successfully", status=status.HTTP_200_OK)


class PasswordRestViewSet(viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=False, methods=["post"])
    def send_reset_email(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not email:
            return Response("No email was given")
        try:
            user_instance = CustomUser.objects.get(email=email)
            user_id = str(user_instance.id)
            expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            payload = {"user_id": user_id, "exp": expiration_time}
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

            send_mail(
                "CSUN Senior Design Password Reset",
                None,
                "CSUN Senior Design <noreply@seniordesignproject.com>",
                [f"{user_instance.email}"],
                html_message=render_to_string(
                    "accounts/password_reset.html", {"token": token}
                ),
                fail_silently=False,
            )
        except ObjectDoesNotExist:
            return Response(
                "If an account with this email exists, a password reset email has been sent.",
                status=status.HTTP_200_OK,
            )
        return Response(
            "If an account with this email exists, a password reset email has been sent.",
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"])
    @transaction.atomic
    def update_password(self, request, *args, **kwargs):
        token = kwargs.get("token", None)
        new_password = request.data.get("new_password")
        if not new_password:
            return Response("New password must be given")
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        except jwt.ExpiredSignatureError:
            return Response(
                "TokenExpiredError",
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except jwt.DecodeError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        user_id = payload["user_id"]
        user_instance = get_object_or_404(CustomUser, pk=user_id)
        user_instance.set_password(new_password)
        user_instance.save()

        return Response("password has been changed", status=status.HTTP_202_ACCEPTED)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ["get", "put", "patch", "delete", "head", "options", "trace"]

    @transaction.atomic
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


# # TODO: Delete StudentProfileViewset
# class StudentProfileViewSet(viewsets.ModelViewSet):
#     queryset = StudentProfile.objects.all()
#     serializer_class = StudentProfileSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()

#         request_data_id = request.data.get("id", None)
#         request_data_user = request.data.get("user", None)
#         if request_data_id and request_data_id != str(instance.id):
#             return Response(
#                 "User IDs cannot be changed", status=status.HTTP_400_BAD_REQUEST
#             )
#         if request_data_user and request_data_user != str(instance.user.id):
#             return Response(
#                 "User IDs cannot be changed", status=status.HTTP_400_BAD_REQUEST
#             )

#         serializer = self.get_serializer(instance, data=request.data, partial=True)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @action(detail=True, methods=["post"])
#     def join_project(self, request, pk=None):
#         try:
#             student_profile = self.get_object()
#         except Http404:
#             return Response(
#                 "Student profile not found", status=status.HTTP_404_NOT_FOUND
#             )
#         project_id = request.data.get("project")
#         if project_id is None:
#             return Response("Missing project_id", status=status.HTTP_400_BAD_REQUEST)
#         try:
#             project_id = int(project_id)
#             if project_id <= 0:
#                 raise ValueError()
#         except ValueError:
#             return Response("Invalid project_id", status=status.HTTP_400_BAD_REQUEST)
#         try:
#             project = Project.objects.get(pk=project_id)
#         except ObjectDoesNotExist:
#             return Response("Project does not exist", status=status.HTTP_404_NOT_FOUND)
#         try:
#             student_profile.join_project(project)
#         except ValidationError as e:
#             return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

#         serializer = StudentProfileSerializer(student_profile)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     @action(detail=True, methods=["post"])
#     def leave_project(self, request, pk=None):
#         try:
#             student_profile = self.get_object()
#         except Http404:
#             return Response(
#                 "Student profile not found", status=status.HTTP_404_NOT_FOUND
#             )
#         try:
#             student_profile.leave_project()
#         except ValidationError as e:
#             return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

#         serializer = StudentProfileSerializer(student_profile)
#         return Response(serializer.data, status=status.HTTP_200_OK)


class ProfessorProfileViewSet(viewsets.ModelViewSet):
    queryset = ProfessorProfile.objects.all()
    serializer_class = ProfessorProfileSerializer
    http_method_names = ["get"]


class ProfessorDashboardViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = ProfessorProfile.objects.all()
    serializer_class = ProfessorProfileSerializer

    def dashboard(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response(
                {
                    "error": "Unauthorized action. You must be logged in to view the professor dashboard"
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        if not request.user.is_professor:
            return Response(
                {
                    "error": "Unauthorized action. Only professors can view professor dashboard"
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        user_id = kwargs.get("pk", None)
        user_instance = CustomUser.objects.get(id=user_id)
        professor_instance = user_instance.professorprofile
        projects = professor_instance.projects.all()
        students = StudentProfile.objects.filter(project__in=projects).distinct()

        student_serializer = ProfessorDashboardStudentSerializer(students, many=True)
        project_serializer = ProfessorDashboardProjectSerializer(projects, many=True)

        return Response(
            {"students": student_serializer.data, "projects": project_serializer.data},
            status=status.HTTP_200_OK,
        )

    def students(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response(
                {
                    "error": "Unauthorized action. You must be logged in to view the professor dashboard"
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        if not request.user.is_professor:
            return Response(
                {
                    "error": "Unauthorized action. Only professors can view professor dashboard"
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        user_id = kwargs.get("pk", None)
        user_instance = CustomUser.objects.get(id=user_id)
        professor_instance = user_instance.professorprofile
        projects = professor_instance.projects.all()
        students = StudentProfile.objects.filter(project__in=projects).distinct()

        student_serializer = ProfessorDashboardStudentSerializer(students, many=True)

        return Response(
            {"students": student_serializer.data}, status=status.HTTP_200_OK
        )

    def projects(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response(
                {
                    "error": "Unauthorized action. You must be logged in to view the professor dashboard"
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        if not request.user.is_professor:
            return Response(
                {
                    "error": "Unauthorized action. Only professors can view professor dashboard"
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        user_id = kwargs.get("pk", None)
        user_instance = CustomUser.objects.get(id=user_id)
        professor_instance = user_instance.professorprofile
        projects = professor_instance.projects.all()

        project_serializer = ProfessorDashboardProjectSerializer(projects, many=True)

        return Response(
            {"projects": project_serializer.data},
            status=status.HTTP_200_OK,
        )


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            user_instance = self.get_object()

            if user_instance.is_student:
                return UserProfileStudentSerializer
            elif user_instance.is_professor:
                return UserProfileProfessorSerializer
        return CustomUserSerializer

    @action(detail=False, methods=["get"])
    def retrieve_user_profile(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response(
                {
                    "error": "Unauthorized action. You must be logged in to view your profile"
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        user_instance = request.user

        if user_instance.is_student:
            student_profile = user_instance.studentprofile
            serializer = UserProfileStudentSerializer(student_profile)
        elif user_instance.is_professor:
            professor_profile = user_instance.professorprofile
            serializer = UserProfileProfessorSerializer(professor_profile)
        else:
            return Response(
                "User role not recognized", status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response(
                {
                    "error": "Unauthorized action. You must be logged in to update your profile"
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        user_id = kwargs.get("pk")

        if not user_id:
            return Response(
                {"error": "Valid user ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_instance = get_object_or_404(CustomUser, pk=user_id)

        if request.user != user_instance:
            return Response(
                {
                    "error": "Unauthorized action. You cannot update another user's profile."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if "id" in request.data:
            return Response(
                {"ID can not be altered"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if "first_name" in request.data or "last_name" in request.data:
            return Response(
                {
                    "First and last name are determined by user's email"
                    + " address and cannot be updated."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if "email" in request.data:
            return Response(
                {"Email addresses cannot be updated."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if "csun_faculty_page_link" in request.data:
            return Response(
                {"Faculty links are determined automatically and cannot be updated."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if "projects" in request.data or "project" in request.data:
            return Response(
                {"Projects can be updated at the /projects/ endpoint."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().update(request, *args, **kwargs)
