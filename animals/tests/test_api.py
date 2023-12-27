from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from animals.models import Animals, FormAnimals, Images
from users.models import EmailVerifications, Users


class AnimalsAPITestCase(APITestCase):
    def setUp(self):
        """data for test db"""

        self.user = Users.objects.create_user(
            email="nikitamisha@gmail.com", password="pogosweb"
        )
        self.access_token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        self.image = Images.objects.create(
            name="chi",
            image="https://img.freepik.com/free-photo/young-adult-enjoying-yoga-in-nature_23-2149573175.jpg",
        )

        data = {
            "name": "Chi",
            "species": "Cha",
            "age": 7,
            "content": "Chi for Cha",
            "user": self.user,
        }
        self.animal = Animals.objects.create(**data)
        self.animal.images.add(self.image)

    def test_animal_create(self):
        """This test covers create animals"""

        url = reverse("animals:animals-list")
        data = {
            "name": "Chi",
            "species": "Cha",
            "age": 7,
            "content": "Chi for Cha",
            "images": [self.image.id],
            "user": self.user.id,
        }
        response = self.client.post(url, data)
        expected_data = 2

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Animals.objects.count(), expected_data)
        self.assertEqual(response.data["name"], "Chi")

    def test_animal_list(self):
        """This test covers list animals"""

        url = reverse("animals:animals-list")
        response = self.client.get(url)
        expected_data = 1

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Animals.objects.count(), expected_data)

    def test_animal_detail(self):
        """This test covers detail animals"""

        url = f"{settings.DOMAIN_NAME}/api/animals/{self.animal.id}/"
        response = self.client.get(url)
        expected_data = 1

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Animals.objects.count(), expected_data)
        self.assertEqual(response.data["name"], "Chi")
        self.assertEqual(len([response.data]), expected_data)

    def test_animal_partial_update(self):
        """This test covers partial update for animals"""

        url = f"{settings.DOMAIN_NAME}/api/animals/{self.animal.id}/"
        data = {"name": "Cha"}
        response = self.client.patch(url, data)
        expected_data = 1

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Animals.objects.count(), expected_data)

    def test_animal_destroy(self):
        """This test covers delete animals"""

        url = f"{settings.DOMAIN_NAME}/api/animals/{self.animal.id}/"
        response = self.client.delete(url)
        expected_data = 0

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Animals.objects.count(), expected_data)


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
        url = reverse("animals:form-create")
        data = {"phone": "+79136757877", "animal": self.animal.id, "user": self.user.id}
        response = self.client.post(url, data)
        expected_data = 1

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FormAnimals.objects.count(), expected_data)
