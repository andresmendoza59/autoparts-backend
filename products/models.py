from django.db import models


class Product(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()

    class Meta:
        db_table = 'products'
