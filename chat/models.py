from django.db import models
from users.models import Users


class Message(models.Model):
    """Model for message"""

    text = models.TextField()
    sent_by = models.CharField(max_length=255)
    created_by = models.ForeignKey(Users, blank=True, null=True,  on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.sent_by}"


class Room(models.Model):
    """Model for room"""
    
    WAITING = "waiting"
    ACTIVE = "active"
    CLOSED = "closed"

    CHOICES_STATUS = (
        (WAITING, "Waiting"),
        (ACTIVE, "Active"),
        (CLOSED, "Closed"),
    )

    uuid = models.CharField(max_length=255)
    client = models.CharField(max_length=255)
    agent = models.ForeignKey(Users, related_name="rooms", blank=True, null=True, on_delete=models.SET_NULL)
    messages = models.ManyToManyField(Message, blank=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default=WAITING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.client} - {self.uuid}"