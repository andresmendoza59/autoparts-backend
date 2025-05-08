from django.db import models


class Workshop(models.Model):
    _id = models.ObjectIdField()
    user = models.ForeignKey('User', on_delete=models.CASCADE)  # Relación con User
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    coordinates = models.CharField(max_length=100)

    class Meta:
        db_table = 'workshops'


class WorkshopProduct(models.Model):
    _id = models.ObjectIdField()
    workshop = models.ForeignKey('Workshop', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'workshop_products'
