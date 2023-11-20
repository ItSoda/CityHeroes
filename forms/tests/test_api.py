# from rest_framework.test import APITestCase
# from django.urls import reverse
# from animals.models import Animals, Images
# from users.models import Users
# from rest_framework import status
# from forms.models import FormAnimals
# from rest_framework_simplejwt.tokens import RefreshToken


# class FormAnimalAPITestCase(APITestCase):
#     def setUp(self):
#         self.image = Images.objects.create(
#             name="niggs",
#             image="https://img.freepik.com/free-photo/young-adult-enjoying-yoga-in-nature_23-2149573175.jpg"
#         )
#         self.user = Users.objects.create_user(
#             email="nikitatopchik@gmail.com", password="pogosweb", is_company=True
#         )

#         self.client.force_authenticate(user=self.user)

#         data = {
#             "id": 1,
#             "name": "ChaCha",
#             "species": "Дворняжка",
#             "age": 7,
#             "content": "крутая дворняжка",
#             "user": self.user.id,
#             "images": [self.image.id]
#         }
#         url=reverse("animals:animals-list")
#         self.animal = self.client.post(url, data).data
#         print(self.animal)

#     def test_create_form_animal(self):
#         url = reverse("forms:form-create")
#         data = {
#             "phone": "+79136757877",
#             "animal": self.animal.id,
#             "user": self.user.id
#         }
#         response = self.client.post(url, data)
#         expected_data = 1

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(FormAnimals.objects.count(), expected_data)
