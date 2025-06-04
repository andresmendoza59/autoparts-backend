from ninja_extra import ControllerBase, api_controller, route
from .schemas import WorkshopSchema, CreateWorkshopSchema
from django.shortcuts import get_object_or_404
from workshops.models import Workshop
from django.http import HttpRequest
from django.db.utils import IntegrityError
from ninja.errors import HttpError


@api_controller('/workshops', tags=["Workshops"])
class WorkshopController(ControllerBase):

    @route.get("/all", response=list[WorkshopSchema])
    def get_all_workshops(self):
        return [
        {
            "id": workshop.id,
            "user_id": workshop.user.id,
            "name": workshop.name,
            "address": workshop.address,
            "coordinates": workshop.coordinates,
        }
        for workshop in Workshop.objects.all()
    ]

    @route.get('/workshop/{workshop_id}', response=WorkshopSchema)
    def get_workshop(self, request: HttpRequest, workshop_id: int):
        workshop = get_object_or_404(Workshop, id=workshop_id)
        return workshop

    @route.post("/add-workshop", response={201: CreateWorkshopSchema})
    def create_workshop(self, request: HttpRequest, data: CreateWorkshopSchema):
        try:
            workshop = Workshop.objects.create(
                user = request.user,
                name = data.name,
                address = data.address,
                coordinates = data.coordinates
            )
            return workshop
        except IntegrityError:
            raise HttpError(409, "A workshop with that name and address already exists")
