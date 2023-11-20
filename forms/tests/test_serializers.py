# from rest_framework.test import APITestCase
# from animals.models import Animals, Images
# from forms.serializers import FormAnimalSerializer
# from forms.models import FormAnimals
# from users.models import Users

# class FormAnimalSerializerAPITestCase(APITestCase):
#     def setUp(self):
#         self.image = Images.objects.create(
#             name="niggs",
#             image="https://img.freepik.com/free-photo/young-adult-enjoying-yoga-in-nature_23-2149573175.jpg"
#         )
#         self.animal = Animals.objects.create(
#             id=1,
#             name="ChaCha",
#             species="Дворняжка",
#             age=7,
#             content="крутая дворняжка",
#             user=1,
#             images=[self.image.id]
#         )
#         self.user = Users.objects.create_user(
#             email="nikitatopchik@gmail.com", password="pogosweb"
#         )
#         self.form = FormAnimals.objects.create(
#             phone="+79136757877",
#             animal=self.animal.id,
#             user=self.user.id
#             )

#     def test_form_animal_serializer(self):
#         """This test covers UserSerializer"""

#         data = FormAnimalSerializer(self.form).data
#         expected_data = {
#             "id": self.form.id,
#             "phone": self.form.phone,
#             "animal": self.form.animal,
#             "user": self.form.user
#             }
#         self.assertEqual(expected_data, data)
