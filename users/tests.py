from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase


User = get_user_model()


class AuthTests(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.token_url = reverse("token_obtain_pair")
        self.test_user = {"login": "testuser", "password": "testpass123"}

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.test_user)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(login="testuser").exists())

    def test_token_obtainment(self):
        self.client.post(self.register_url, self.test_user)

        response = self.client.post(
            self.token_url, {"login": "testuser", "password": "testpass123"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_verification(self):
        self.client.post(self.register_url, self.test_user)
        token_resp = self.client.post(self.token_url, self.test_user)

        verify_url = reverse("token_verify")
        response = self.client.post(verify_url, {"token": token_resp.data["access"]})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {})


class UserOperationsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            login="moneyuser", password="testpass123", money_balance=100.00
        )
        self.token_url = reverse("token_obtain_pair")

        token_resp = self.client.post(
            self.token_url, {"login": "moneyuser", "password": "testpass123"}
        )
        self.access_token = token_resp.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_add_money(self):
        url = reverse("add-money", kwargs={"user_id": self.user.id})
        response = self.client.post(url, {"amount": 50.00})

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.money_balance, 150.00)

    def test_revoke_tokens(self):
        verify_url = reverse("token_verify")
        verify_resp = self.client.post(verify_url, {"token": self.access_token})
        self.assertEqual(verify_resp.status_code, 200)

        revoke_url = reverse("revoke-tokens", kwargs={"user_id": self.user.id})
        revoke_resp = self.client.post(revoke_url)
        self.assertEqual(revoke_resp.status_code, 200)

        verify_resp = self.client.post(verify_url, {"token": self.access_token})
        self.assertEqual(verify_resp.status_code, 401)


class TokenVersionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            login="tokenuser", password="testpass123", token_version=1
        )
        self.token_url = reverse("token_obtain_pair")
        token_resp = self.client.post(
            self.token_url, {"login": "tokenuser", "password": "testpass123"}
        )
        self.access_token = token_resp.data["access"]

    def test_token_version_check(self):
        verify_url = reverse("token_verify")

        response = self.client.post(verify_url, {"token": self.access_token})
        self.assertEqual(response.status_code, 200)

        self.user.token_version = 2
        self.user.save()

        response = self.client.post(verify_url, {"token": self.access_token})
        self.assertEqual(response.status_code, 401)
        self.assertIn("Token revoked", str(response.data["detail"]))
