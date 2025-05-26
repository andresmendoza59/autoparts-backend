from ninja import Schema
from django.contrib.auth.models import User

class CreateWorkshopSchema(Schema):
    name: str
    address: str
    coordinates: str

class WorkshopSchema(Schema):
    id: int
    user_id: int
    name: str
    address: str
    coordinates: str
