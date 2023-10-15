from django.contrib import admin
from .models import Project  # Import the Project model

# Define the admin class
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'open_slots', 'capacity')  # Customize which fields to display
    list_filter = ('open_slots', 'capacity')  # Customize filters
    search_fields = ('project_name',)  # Customize search fields

# Register the admin class with the model
admin.site.register(Project, ProjectAdmin)
