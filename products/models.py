from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    photo = models.ImageField(upload_to='media/products', default='')

    class Meta:
        unique_together = ('name', 'price', 'description')
