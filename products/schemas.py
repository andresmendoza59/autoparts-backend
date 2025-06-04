from ninja import Schema
from typing import Optional


class ProductSchema(Schema):
    name: str
    price: float
    description: str
    photo: Optional[str] = None
