# Generated by Django 4.2 on 2023-12-31 07:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_alter_users_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="users",
            name="photo",
            field=models.ImageField(
                default="user_images/no-profile.png", upload_to="user_images"
            ),
        ),
    ]
