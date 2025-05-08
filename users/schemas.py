from ninja import Schema


class UserCreateSchema(Schema):
    username: str
    password: str


class UserDetailSchema(Schema):
    username: str
