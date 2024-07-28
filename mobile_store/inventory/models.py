from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    nationality = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Mobile(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.CharField(max_length=100, unique=True)
    price = models.PositiveIntegerField()
    color = models.CharField(max_length=50)
    screen_size = models.PositiveIntegerField()
    STATUS_CHOICES = [
        ('+', 'موجود'),
        ('-', 'ناموجود')
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    manufacturer_country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.brand} {self.model}"
