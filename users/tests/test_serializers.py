from rest_framework.test import APITestCase

from users.models import Users
from users.serializers import UserRegistSerializer, UserSerializer


class SerializersUsersAPITest(APITestCase):
    def setUp(self):
        """data for test db"""

        self.user_1 = Users.objects.create_user(
            username="koker1", email="nikita@gmail.com", password="nik140406"
        )
        self.user_2 = Users.objects.create_user(
            username="koker12", email="nikitaaa@gmail.com", password="nik14040666"
        )

        self.user_company_1 = Users.objects.create_user(
            username="koker13",
            email="nikitaalaf@gmail.com",
            password="nik140406",
            is_company=True,
        )

    # def test_user_serializer(self):
    #     """This test covers UserSerializer"""

    #     data = UserSerializer([self.user_1, self.user_2], many=True).data
    #     expected_data = [
    #         {
    #             "id": self.user_1.id,
    #             "username": self.user_1.username,
    #             "photo": self.user_1.photo,
    #         },
    #         {
    #             "id": self.user_2.id,
    #             "username": self.user_2.username,
    #             "photo": self.user_2.photo,
    #         },
    #     ]
    #     self.assertEqual(expected_data, data)

    def test_user_register_serializer(self):
        """This test covers UserCompanyCreateSerializer"""

        data = UserRegistSerializer(self.user_company_1).data
        expected_data = (
            {
                "id": self.user_company_1.id,
                "email": "nikitaalaf@gmail.com",
                "username": self.user_company_1.username,
            },
        )
        self.assertEqual(expected_data[0], data)
