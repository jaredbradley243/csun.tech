from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "email",
        "first_name",
        "last_name",
        "student_id",
        "is_staff",
        "is_professor",
        "is_team_lead",
        "is_student",
        "email_confirmed",
        "is_volunteer",
        "is_active",
    )

    list_filter = (
        "is_staff",
        "is_professor",
        "is_team_lead",
        "is_student",
        "email_confirmed",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "student_id")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_professor",
                    "is_team_lead",
                    "is_student",
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
                    "student_id",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_team_lead",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

    def is_volunteer(self, obj):
        return obj.userprofile.is_volunteer

    is_volunteer.boolean = True
    is_volunteer.short_description = "Volunteer"
    is_volunteer.admin_order_field = "userprofile__is_volunteer"


admin.site.register(CustomUser, CustomUserAdmin)
