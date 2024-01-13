from django.contrib import admin
from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from accounts.views import (
    CustomUserViewSet,
    # StudentProfileViewSet,
    ProfessorDashboardViewSet,
    ProfessorProfileViewSet,
    UserProfileViewSet,
    RegistrationViewSet,
    EmailVerificationViewSet,
    LoginViewSet,
    PasswordRestViewSet,
)
from projects.views import ProjectsViewSet

router = DefaultRouter()
router.register(r"projects", ProjectsViewSet)

# TODO: Delete users router
router.register(r"users", CustomUserViewSet)

# TODO: Delete students router
# router.register(r"students", StudentProfileViewSet)

# TODO: Delete professorprofiles router
# router.register(r"professorprofiles", ProfessorProfileViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("register/", RegistrationViewSet.as_view({"post": "create"})),
    path("login/", LoginViewSet.as_view()),
    path(
        "emailverification/",
        EmailVerificationViewSet.as_view({"get": "verify"}),
    ),
    path(
        "emailverification/<str:token>/",
        EmailVerificationViewSet.as_view({"get": "verify"}),
    ),
    path(
        "resendverificationemail/<uuid:pk>/",
        EmailVerificationViewSet.as_view({"get": "resend"}),
    ),
    path(
        "passwordreset/",
        PasswordRestViewSet.as_view({"post": "send_reset_email"}),
    ),
    path(
        "passwordreset/<str:token>/",
        PasswordRestViewSet.as_view({"post": "update_password"}),
    ),
    path(
        "projects/students/<str:user_id>/",
        ProjectsViewSet.as_view({"delete": "leave_project"}),
    ),
    path(
        "projects/<int:pk>/professors/<str:user_id>/",
        ProjectsViewSet.as_view({"delete": "professor_leave_project"}),
    ),
    path(
        "professors/<uuid:pk>/dashboard/",
        ProfessorDashboardViewSet.as_view({"get": "dashboard"}),
    ),
    path(
        "professors/<uuid:pk>/students/",
        ProfessorDashboardViewSet.as_view({"get": "students"}),
    ),
    path(
        "professors/<uuid:pk>/projects/",
        ProfessorDashboardViewSet.as_view({"get": "projects"}),
    ),
    path("userprofile/", UserProfileViewSet.as_view({"get": "retrieve_user_profile"})),
    path(
        "userprofile/<uuid:pk>",
        UserProfileViewSet.as_view({"put": "update"}),
    ),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
