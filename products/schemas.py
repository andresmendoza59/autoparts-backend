from ninja import Schema


class ProductSchema(Schema):
    name: str
    price: float
    description: str
