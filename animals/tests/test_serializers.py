from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from animals.models import Animals, Images
from animals.serializers import AnimalSerializer
from users.models import Users


class AnimalSerializersAPITestCase(APITestCase):
    def setUp(self):
        """data for test db"""
        self.user = Users.objects.create_user(
            email="nikitamisha@gmail.com", password="pogosweb", is_company=True
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

    def test_animal_serializer(self):
        """This test covers AnimalSerializer"""

        data = AnimalSerializer(self.animal).data
        expected_data = {
            "id": self.animal.id,
            "name": "Chi",
            "species": "Cha",
            "age": 7,
            "content": "Chi for Cha",
        }

        self.assertEqual(data, expected_data)
