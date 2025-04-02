from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from scripts.models import Project, Script
from scripts import serializers


class ProjectsViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(owner_id=self.request.user.id)


class ScriptsViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ScriptSerializer

    def get_queryset(self):
        project_id = self.kwargs["project_id"]

        project = get_object_or_404(
            Project.objects.filter(owner=self.request.user), id=project_id
        )
        return Script.objects.filter(parent_project=project)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["project_id"] = self.kwargs["project_id"]
        return context
