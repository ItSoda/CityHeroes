# from rest_framework.test import APITestCase

# from users.models import Users
# from users.serializers import UserCompanySerializer, UserSerializer


# class SerializersUsersAPITest(APITestCase):
#     def setUp(self):
#         """data for test db"""

#         self.user_1 = Users.objects.create_user(
#             email="nikita@gmail.com", password="nik140406"
#         )
#         self.user_2 = Users.objects.create_user(
#             email="nikitaaa@gmail.com", password="nik14040666"
#         )

#         self.user_company_1 = Users.objects.create_user(
#             email="nikitaalaf@gmail.com", password="nik140406", is_company=True
#         )

#     def test_user_serializer(self):
#         """This test covers UserSerializer"""

#         data = UserSerializer([self.user_1, self.user_2], many=True).data
#         print(data)
#         print()
#         expected_data = [
#             {
#                 "id": self.user_1.id,
#                 "email": "nikita@gmail.com",
#             },
#             {
#                 "id": self.user_2.id,
#                 "email": "nikitaaa@gmail.com",
#             },
#         ]
#         print(expected_data)
#         self.assertEqual(expected_data, data)

#     def test_user_company_create_serializer(self):
#         """This test covers UserCompanyCreateSerializer"""

#         data = UserCompanySerializer(self.user_company_1).data
#         expected_data = (
#             {
#                 "id": self.user_company_1.id,
#                 "email": "nikitaalaf@gmail.com",
#                 "name_company": "ChangeCompanyName",
#                 "is_company": True,
#                 "description": None,
#             },
#         )
#         self.assertEqual(expected_data[0], data)
