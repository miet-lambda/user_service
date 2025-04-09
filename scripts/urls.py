from django.urls import path, include
from rest_framework import routers
from scripts.api import ScriptsViewSet, ProjectsViewSet



router = routers.SimpleRouter()
router.register(r"", ProjectsViewSet, basename="project")

urlpatterns = [
    path("", include(router.urls)),

    path(
        "<int:project_id>/scripts/",
        ScriptsViewSet.as_view({"get": "list", "post": "create"}),
        name="project-scripts",
    ),

    path(
        "<int:project_id>/scripts/<int:pk>/",
        ScriptsViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="project-script-detail",
    ),
]
