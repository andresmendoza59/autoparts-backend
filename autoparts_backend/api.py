from ninja import NinjaAPI, Schema
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth
from ninja_extra import NinjaExtraAPI

from workshops.api import WorkshopController


api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)
api.register_controllers(WorkshopController)

class UserSchema(Schema):
    username: str
    is_authenticated: bool
    email: str = None


@api.get("/hello")
def hello(request) -> str:
    print(request)
    return "Hello World!"


@api.get("/me", response=UserSchema, auth=JWTAuth())
def me(request) -> UserSchema:
    return request.user
