from ninja import Schema


class WorkshopSchema(Schema):
    user: str
    name: str
    address: str
