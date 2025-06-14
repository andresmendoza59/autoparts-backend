from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Workshop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    coordinates = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='media/workshops', default='')

    class Meta:
        unique_together = ('name', 'address')


class WorkshopProduct(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
