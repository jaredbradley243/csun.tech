"""csuntech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    UserProfileViewSet,
    StudentProfileViewSet,
    ProfessorProfileViewSet,
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
router.register(r"userprofiles", UserProfileViewSet)
router.register(r"studentprofiles", StudentProfileViewSet)
router.register(r"professorprofiles", ProfessorProfileViewSet)
router.register(r"projects", ProjectsViewSet)
urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
]
