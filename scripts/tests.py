from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status
from scripts.models import Project, Script

User = get_user_model()


class ScriptAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(login="testuser", password="testpass123")

        self.project = Project.objects.create(name="Test Project", owner=self.user)

        self.client.force_authenticate(user=self.user)

        self.scripts_url = reverse(
            "project-scripts", kwargs={"project_id": self.project.id}
        )
        self.script_detail_url = lambda pk: reverse(
            "project-script-detail", kwargs={"project_id": self.project.id, "pk": pk}
        )

    def test_create_script(self):
        data = {"path": "main.py", "source_code": 'print("Hello")'}

        response = self.client.post(self.scripts_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Script.objects.count(), 1)
        self.assertEqual(Script.objects.get().path, "main.py")

    def test_unique_script_path(self):
        Script.objects.create(
            path="main.py", source_code="code1", parent_project=self.project
        )

        data = {"path": "main.py", "source_code": "code2"}

        response = self.client.post(self.scripts_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("A script with this path already exists", str(response.data))

    def test_partial_update_script(self):
        script = Script.objects.create(
            path="old.py", source_code="old code", parent_project=self.project
        )

        update_data = {"source_code": "new code"}

        response = self.client.patch(self.script_detail_url(script.id), update_data)

        script.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(script.source_code, "new code")
        self.assertEqual(script.path, "old.py")

    def test_list_scripts(self):
        Script.objects.create(
            path="script1.py", source_code="code1", parent_project=self.project
        )
        Script.objects.create(
            path="script2.py", source_code="code2", parent_project=self.project
        )

        response = self.client.get(self.scripts_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["path"], "script1.py")

    def test_delete_script(self):
        script = Script.objects.create(
            path="to_delete.py", source_code="delete me", parent_project=self.project
        )

        response = self.client.delete(self.script_detail_url(script.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Script.objects.count(), 0)

    def test_foreign_project_access(self):
        other_user = User.objects.create_user(login="otheruser", password="otherpass")
        other_project = Project.objects.create(name="Other Project", owner=other_user)

        url = reverse("project-scripts", kwargs={"project_id": other_project.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_update_script(self):
        script = Script.objects.create(
            path="original.py", source_code="original code", parent_project=self.project
        )

        update_data = {"path": "updated.py"}

        response = self.client.put(self.script_detail_url(script.id), update_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("source_code", response.data)
