from djongo import models
from django.contrib.auth.models import AbstractUser

from djongo import models

class User(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)  # Puedes usar hashing luego
    role = models.CharField(max_length=20, choices=[('vendedor', 'Vendedor'), ('comprador', 'Comprador')])
    email = models.EmailField(unique=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name


class Workshop(models.Model):
    _id = models.ObjectIdField()
    user = models.ForeignKey('User', on_delete=models.CASCADE)  # Relación con User
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    coordinates = models.CharField(max_length=100)

    class Meta:
        db_table = 'workshops'


class Product(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()

    class Meta:
        db_table = 'products'


class WorkshopProduct(models.Model):
    _id = models.ObjectIdField()
    workshop = models.ForeignKey('Workshop', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'workshop_products'
