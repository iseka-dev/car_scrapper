from django.db import models


class Car(models.Model):

    maker = models.CharField(
        max_length=25,
    )
    model = models.CharField(
        max_length=100,
    )
    price = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
