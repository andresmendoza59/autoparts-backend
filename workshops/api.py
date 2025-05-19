from ninja import Router
from .schemas import WorkshopSchema
from django.shortcuts import get_object_or_404

from workshops.models import Workshop

router = Router()


@router.get(f'/workshop/{workshop_id}', response_model=WorkshopSchema)
def get_workshop(request, workshop_id: int):
    workshop = get_object_or_404(Workshop.objects.get(Workshop, id=workshop_id))
    return workshop
