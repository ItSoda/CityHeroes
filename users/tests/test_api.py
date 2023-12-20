from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import EmailVerifications, Users


class UsersAPITestCase(APITestCase):
    def setUp(self):
        """data for test db"""

        self.superuser = Users.objects.create_superuser(
            email="nikitatop@gmail.com", password="nikitatop23"
        )
        self.user_2 = Users.objects.create_user(
            email="nikitatopchik@gmail.com", password="nikitatop23"
        )
        self.access_token = str(RefreshToken.for_user(self.superuser).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_create_account(self):
        """This test covers user registration and verification for sending email"""

        url = reverse("users:users-list")
        data = {"username": "nikita", "email": "nikitashchegilskiy@gmail.com", "password": "nikitaWeb123"}
        response = self.client.post(url, data)
        expected_data = 3

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Users.objects.count(), expected_data)
        self.assertEqual(
            Users.objects.get(email=response.data["email"]).is_company, False
        )
        self.assertEqual(EmailVerifications.objects.count(), expected_data)

    def test_create_company_account(self):
        """This test covers company account registration and verification for sending email"""

        url = reverse("users:users-list")
        data = {
            "email": "pogosweb@gmail.com",
            "password": "PogosProfi123",
            "is_company": True,
        }
        response = self.client.post(url, data)
        expected_data = 3

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Users.objects.count(), expected_data)
        self.assertEqual(EmailVerifications.objects.count(), expected_data)

    def test_login_account(self):
        """This test covers user account login"""

        url = reverse("token_obtain_pair")
        data = {"email": self.superuser.email, "password": "nikitatop23"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_account(self):
        """This test covers user account logout"""

        url = reverse("token_blacklist")
        self.refresh_token = str(RefreshToken.for_user(self.superuser))
        self.access_token = str(RefreshToken.for_user(self.superuser).access_token)
        data = {"refresh": self.refresh_token}
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        invalid_response = self.client.post(reverse("token_blacklist"), data)
        self.assertEqual(invalid_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_list(self):
        """This test covers users list"""

        url = reverse("users:users-list")
        response = self.client.get(url)
        expected_data_length = 2

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), expected_data_length)

    def test_profile_company_account(self):
        """This test covers company account profile"""

        url = f"{settings.DOMAIN_NAME}/auth/users/me/"
        response = self.client.get(url)
        expected_data = 1

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.superuser.email)
        self.assertEqual(len([response.data]), expected_data)
