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
    StudentProfileViewSet,
    ProfessorDashboardViewSet,
    ProfessorProfileViewSet,
    UserProfileViewSet,
    #     # RegisterViewSet,
)
from projects.views import ProjectsViewSet

router = DefaultRouter()
router.register(r"users", CustomUserViewSet)
# router.register(r"userprofile", UserProfileViewSet, basename="userprofile")
router.register(r"students", StudentProfileViewSet)
router.register(r"professorprofiles", ProfessorProfileViewSet)
router.register(r"projects", ProjectsViewSet)
# router.register(r"register", RegisterViewSet, basename="register")

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path(
        "projects/students/<str:user_id>/",
        ProjectsViewSet.as_view({"delete": "leave_project"}),
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

# TODO - Create email verification endpoint to send users when
# they click link in verification email

# TODO - Create login endpoint for users to login
# 1) Check for email_confirmed value of True
# 2) Check for JWT token
