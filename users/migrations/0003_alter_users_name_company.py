# Generated by Django 4.2 on 2023-11-20 14:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_users_name_company"),
    ]

    operations = [
        migrations.AlterField(
            model_name="users",
            name="name_company",
            field=models.CharField(
                default="ChangeCompanyName", max_length=150, null=True
            ),
        ),
    ]