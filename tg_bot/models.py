from django.db import models


# БД для хранения данных о пользователях
class Tg_Bot(models.Model):
    """Model for one Tg_Bot"""

    user_id = models.IntegerField(verbose_name="USER ID", unique=True)

    username = models.CharField(max_length=256, null=True, blank=True)

    first_name = models.CharField(
        verbose_name="Name",
        max_length=256,
    )

    last_name = models.CharField(max_length=256, null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "тг_бот"
        verbose_name_plural = "ТГ_БОТ"


class News(models.Model):
    text = models.TextField()
    photo = models.ImageField(upload_to="news_bot_images", null=True, blank=True)

    class Meta:
        verbose_name = "новость"
        verbose_name_plural = "Новости"