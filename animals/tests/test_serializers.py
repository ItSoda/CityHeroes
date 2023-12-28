from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from animals.models import Animals, FormAnimals, Images
from animals.serializers import (AnimalSerializer, FormAnimalSerializer,
                                 ImageSerializer)
from users.models import Users
from users.serializers import UserSerializer


class AnimalSerializersAPITestCase(APITestCase):
    def setUp(self):
        """data for test db"""
        self.user = Users.objects.create_user(
            email="nikitamisha@gmail.com", password="pogosweb", is_company=True
        )
        self.access_token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        self.image = Images.objects.create(
            title="chi",
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

    def test_animal_serializer(self):
        """This test covers AnimalSerializer"""

        data = AnimalSerializer(self.animal).data
        self.user = UserSerializer(self.user).data
        self.image = ImageSerializer(self.image).data
        expected_data = {
            "id": self.animal.id,
            "name": "Chi",
            "species": "Cha",
            "age": 7,
            "content": "Chi for Cha",
            "user": self.user,
            "images": [self.image],
        }

        self.assertEqual(data, expected_data)


class FormAnimalSerializerAPITestCase(APITestCase):
    def setUp(self):
        """data for test db"""

        self.image = Images.objects.create(
            title="niggs",
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

        data = {"phone": "+79136757877", "user": self.user, "animal": self.animal}
        self.form = FormAnimals.objects.create(**data)

    def test_form_animal_serializer(self):
        """This test covers FormAnimalSerializer"""

        data = FormAnimalSerializer(self.form).data
        self.user = UserSerializer(self.form.user).data
        self.animal = AnimalSerializer(self.form.animal).data
        expected_data = {
            "id": self.form.id,
            "phone": self.form.phone,
            "user": self.user,
            "animal": self.animal,
        }
        self.assertEqual(data, expected_data)
