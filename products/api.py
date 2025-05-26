from ninja_extra import ControllerBase, api_controller, route
from .schemas import ProductSchema
from django.shortcuts import get_object_or_404
from .models import Product
from django.http import HttpRequest
from ninja_jwt.authentication import JWTAuth
from django.db.utils import IntegrityError
from ninja.errors import HttpError


@api_controller('/products', tags=['Products'])
class ProductController(ControllerBase):

    @route.get('/all', response=list[ProductSchema])
    def get_all_products(self):
        return Product.objects.all()
    
    @route.get('/product/{product_id}', response=ProductSchema)
    def get_product(self, product_id: int):
        return get_object_or_404(Product, id=product_id)
    
    @route.post('/add', response={201: ProductSchema}, auth=JWTAuth())
    def add_product(self, request: HttpRequest, data: ProductSchema):
        try:
            product = Product.objects.create(
                name = data.name,
                price = data.price,
                description = data.description
            )
            return product
        except IntegrityError:
            return HttpError(409, 'That product already exists')
