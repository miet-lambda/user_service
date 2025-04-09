from typing import Any
from django.contrib import admin
from scripts.models import Project, Script

class ProjectsAdmin(admin.ModelAdmin):
    fields = ["name"]
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(owner=request.user)

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        obj.owner = request.user
        return super().save_model(request, obj, form, change)

class ScriptsAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(parent_project__owner=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent_project":
            kwargs["queryset"] = Project.objects.all().filter(owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Script, ScriptsAdmin)
admin.site.register(Project, ProjectsAdmin)
