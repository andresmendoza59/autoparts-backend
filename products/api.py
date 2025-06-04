from ninja_extra import ControllerBase, api_controller, route
from .schemas import ProductSchema
from django.shortcuts import get_object_or_404
from .models import Product
from django.http import HttpRequest
from django.db.utils import IntegrityError
from ninja.errors import HttpError
from ninja import UploadedFile, File, Form


@api_controller('/products', tags=['Products'])
class ProductController(ControllerBase):

    @route.get('/all', response=list[ProductSchema])
    def get_all_products(self, request):
        products = Product.objects.all()
        return [
            {
                'id': p.id,
                'name': p.name,
                'price': p.price,
                'description': p.description,
                'photo': request.build_absolute_uri(p.photo.url) if p.photo else None
            }
            for p in products
        ]
    
    @route.get('/product/{product_id}', response=ProductSchema)
    def get_product(self, product_id: int):
        return get_object_or_404(Product, id=product_id)
    
    @route.post('/add', response={201: ProductSchema})
    def add_product(self, request: HttpRequest, name: str=Form(...), price: float=Form(...), description: str=Form(...),
                    photo: UploadedFile=File(...)):
        try:
            product = Product.objects.create(
                name = name,
                price = price,
                description = description,
                photo = photo
            )
            return product
        except IntegrityError:
            return HttpError(409, 'That product already exists')
