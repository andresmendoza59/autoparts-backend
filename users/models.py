from django.db import models


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
