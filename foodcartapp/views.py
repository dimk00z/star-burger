from http.client import NO_CONTENT
import json
from django.http import JsonResponse
from django.templatetags.static import static

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Order, OrderItem

from .models import Product, Order, OrderItem
from .serializers import OrderSerializer


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            },
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(["POST"])
def register_order(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
# @api_view(['POST'])
# def register_order(request):
#     try:
#         print(request.data)
#         order_data = request.data
#         order = Order.objects.create(
#             customer_name=order_data['firstname'],
#             customer_lastname=order_data['lastname'],
#             customer_phonenumber=order_data['phonenumber'],
#             customer_address=order_data['address'])
#         for product in order_data['products']:
#             OrderItem.objects.create(
#                 product_id=product['product'],
#                 quantity=product['quantity'],
#                 order=order,
#             )
#     except (ValueError, TypeError):
#         return Response(order_data, status=status.HTTP_201_CREATED)

#     return Response(None, status=status.HTTP_400_BAD_REQUEST)
