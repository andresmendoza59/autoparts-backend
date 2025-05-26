from ninja import NinjaAPI, Schema
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth
from ninja_extra import NinjaExtraAPI

from workshops.api import WorkshopController


api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)
api.register_controllers(WorkshopController)
