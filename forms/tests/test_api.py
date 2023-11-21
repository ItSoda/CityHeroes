from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from animals.models import Animals, Images
from forms.models import FormAnimals
from users.models import EmailVerifications, Users


class FormAnimalAPITestCase(APITestCase):
    def setUp(self):
        """data for test db"""

        self.image = Images.objects.create(
            name="niggs",
            image="https://img.freepik.com/free-photo/young-adult-enjoying-yoga-in-nature_23-2149573175.jpg",
        )
        self.user = Users.objects.create_user(
            email="nikitamisha@gmail.com", password="pogosweb", is_company=True
        )
        self.access_token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        data = {
            "name": "Chi",
            "species": "Cha",
            "age": 7,
            "content": "Chi for Cha",
            "user": self.user,
        }
        self.animal = Animals.objects.create(**data)
        self.animal.images.add(self.image)

    def test_create_form_animal(self):
        """This test covers create form animal"""
        url = reverse("forms:form-create")
        data = {"phone": "+79136757877", "animal": self.animal.id, "user": self.user.id}
        response = self.client.post(url, data)
        expected_data = 1

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FormAnimals.objects.count(), expected_data)
        self.assertEqual(EmailVerifications.objects.count(), expected_data)
