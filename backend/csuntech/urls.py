from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views


from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts.views import (
    CustomUserViewSet,
    #     # StudentProfileViewSet,
    #     # ProfessorProfileViewSet,
    #     # ProfessorDashboardViewSet,
    #     # TeamLeadProfileViewSet,
    #     # RegisterViewSet,
)
from projects.views import ProjectsViewSet

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("", accounts_views.index, name="index"),
#     path("register/", accounts_views.register, name="register"),
#     path(
#         "login/",
#         auth_views.LoginView.as_view(template_name="accounts/login.html"),
#         name="login",
#     ),
#     path("logout/", auth_views.LogoutView.as_view(), name="logout"),
# ]

router = DefaultRouter()
router.register(r"users", CustomUserViewSet)
# router.register(r"students", StudentProfileViewSet)
# router.register(r"teamleads", TeamLeadProfileViewSet)
# router.register(r"professors", ProfessorProfileViewSet)
router.register(r"projects", ProjectsViewSet)
# router.register(
#     r"professordashboard", ProfessorDashboardViewSet, basename="professordashboard"
# )
# router.register(r"register", RegisterViewSet, basename="register")

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    # path(
    #     "professordashboard/<str:professor_id>/",
    #     ProfessorDashboardViewSet.as_view({"get": "list"}),
    #     name="professor-dashboard",
    # ),
]

# TODO - Create email verification endpoint to send users when
# they click link in verification email

# TODO - Create login endpoint for users to login
# 1) Check for email_confirmed value of True
# 2) Check for JWT token
