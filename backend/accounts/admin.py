from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StudentProfile, ProfessorProfile
from django.utils.html import format_html


class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = "Student Profiles"


class ProfessorProfileInline(admin.StackedInline):
    model = ProfessorProfile
    can_delete = False
    verbose_name_plural = "Professor Profiles"


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        "email",
        "first_name",
        "last_name",
        "get_student_id",
        "get_team_lead",
        "get_is_volunteer",
        "get_bio",
        "get_resume",
        "get_project",
        "get_rate_my_professor",
        "get_csun_faculty_page",
        "is_staff",
        "email_confirmed",
        "is_active",
    )

    list_filter = (
        "is_staff",
        "email_confirmed",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "email_confirmed",
                    "is_active",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

    def get_inline_instances(self, request, obj=None):
        if obj and hasattr(obj.profile, "studentprofile"):
            self.inlines = [StudentProfileInline]
        elif obj and hasattr(obj.profile, "professorprofile"):
            self.inlines = [ProfessorProfileInline]
        else:
            self.inlines = []
        return super().get_inline_instances(request, obj)

    def get_bio(self, obj):
        return obj.profile.bio

    get_bio.short_description = "Bio"

    def get_team_lead(self, obj):
        if hasattr(obj.profile, "studentprofile"):
            return obj.profile.studentprofile.team_lead
        return None

    get_team_lead.short_description = "Team Lead"

    def get_is_volunteer(self, obj):
        if hasattr(obj.profile, "studentprofile"):
            return obj.profile.studentprofile.is_volunteer
        return None

    get_is_volunteer.short_description = "Is Volunteer"

    def get_resume(self, obj):
        if hasattr(obj.profile, "studentprofile") and obj.profile.studentprofile.resume:
            return format_html(
                "<a href='{}'>Download</a>", obj.profile.studentprofile.resume.url
            )
        return None

    get_resume.short_description = "Resume"

    def get_project(self, obj):
        if hasattr(obj.profile, "studentprofile"):
            return obj.profile.studentprofile.project
        elif hasattr(obj.profile, "professorprofile"):
            return ", ".join(
                [
                    str(project)
                    for project in obj.profile.professorprofile.projects.all()
                ]
            )
        return None

    get_project.short_description = "Project"

    def get_rate_my_professor(self, obj):
        if hasattr(obj.profile, "professorprofile"):
            return obj.profile.professorprofile.rate_my_professor_link
        return None

    get_rate_my_professor.short_description = "Rate My Professor"

    def get_csun_faculty_page(self, obj):
        if hasattr(obj.profile, "professorprofile"):
            return obj.profile.professorprofile.csun_faculty_page_link
        return None

    get_csun_faculty_page.short_description = "CSUN Faculty Page"

    def get_student_id(self, obj):
        if hasattr(obj.profile, "studentprofile"):
            return obj.profile.studentprofile.student_id
        return None


admin.site.register(CustomUser, CustomUserAdmin)
