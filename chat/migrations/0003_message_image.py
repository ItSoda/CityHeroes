# Generated by Django 4.2 on 2023-12-03 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_rename_user_message_sender_personalmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='message_images'),
        ),
    ]