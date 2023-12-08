from django.db import models
from users.models import Users


class Room(models.Model):
    """Model for room"""

    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    host = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="rooms")
    current_users = models.ManyToManyField(
        Users, related_name="current_rooms", blank=True
    )

    def __str__(self):
        return f"Room({self.name} {self.host} {self.id})"


class Message(models.Model):
    """Model for big chat"""

    room = models.ForeignKey("Room", on_delete=models.CASCADE, related_name="messages")
    text = models.TextField(max_length=500)
    sender = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="messages")
    image = models.ImageField(upload_to='message_images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message({self.sender} {self.room})"


class PersonalMessage(models.Model):
    """Model for personal messages"""

    sender = models.ForeignKey(to=Users, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(to=Users, on_delete=models.CASCADE, related_name="received_messages")
    text = models.TextField()
    image = models.ImageField(upload_to='message_images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)