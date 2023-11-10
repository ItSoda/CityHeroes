from django.db import models


# БД для хранения данных о пользователях
class TG_USER(models.Model):
    user_id = models.IntegerField(
        verbose_name='USER ID',
        unique=True
    )

    username = models.CharField(
        max_length=256, 
        null=True, 
        blank=True
        )
    
    first_name = models.CharField(
        verbose_name='Name',
        max_length=256,
        )
    
    last_name = models.CharField(
        max_length=256,
        null=True, 
        blank=True
        )
    
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)