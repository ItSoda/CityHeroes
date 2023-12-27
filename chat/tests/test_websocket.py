# from channels.layers import get_channel_layer
# from channels.testing import WebsocketCommunicator
# from django.test import TestCase
# import json
# from chat.consumers import RoomConsumer # Замените на вашего консьюмера

# class YourConsumerTest(TestCase):
#     async def connect_ws(self):
#         # Создаем экземпляр канального слоя
#         channel_layer = get_channel_layer()

#         # Создаем коммуникатор для работы с веб-сокетом
#         communicator = WebsocketCommunicator(RoomConsumer.as_asgi(), "ws/chat/")

#         # Устанавливаем соединение
#         connected, _ = await communicator.connect()
#         self.assertTrue(connected)

#         return communicator

#     async def disconnect_ws(self, communicator):
#         # Закрываем соединение
#         await communicator.disconnect()

#     async def send_and_receive(self, communicator, message):
#         # Отправляем и получаем сообщения
#         await communicator.send_json_to(message)
#         response = await communicator.receive_json_from()
#         return response

#     async def test_your_consumer(self):
#         communicator = await self.connect_ws()

#         try:
#             # Ваши тестовые действия с веб-сокетом
#             message = {
#                 "type": "text.message",
#                 "content": "Hello, WebSocket!",
#             }

#             response = await self.send_and_receive(communicator, message)

#             self.assertEqual(response, {"type": "text.message", "content": "Hello, WebSocket!"})

#         finally:
#             await self.disconnect_ws(communicator)