from rest_framework import serializers
from scripts.models import Project, Script


class ProjectSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = self.context["request"].user
        project = Project.objects.create(
            name=validated_data["name"],
            owner_id=user.id,
        )
        return project

    class Meta:
        model = Project
        fields = ("id", "name", "owner_id")


class ScriptSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        project_id = self.context["project_id"]
        instance = self.instance

        if "path" in attrs:
            if (
                Script.objects.filter(parent_project_id=project_id, path=attrs["path"])
                .exclude(pk=instance.pk if instance else None)
                .exists()
            ):
                raise serializers.ValidationError(
                    "A script with this path already exists"
                )
        return attrs

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def create(self, validated_data):
        return Script.objects.create(
            path=validated_data["path"],
            source_code=validated_data["source_code"],
            parent_project_id=self.context["project_id"],
        )

    class Meta:
        model = Script
        fields = ("id", "path", "source_code", "parent_project_id")
