from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)

    # TODO: добавити CRUD для добавлення в улюблені + сторінку улюблених (вибраних) товарів
    favourites = models.ManyToManyField(
        "shop.Product",
        related_name="favourited_by",
        blank=True
    )

    def __str__(self):
        return self.user.username

