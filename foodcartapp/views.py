from http.client import NO_CONTENT

from django.http import JsonResponse
from django.templatetags.static import static

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer


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
@renderer_classes((JSONRenderer, BrowsableAPIRenderer))
def register_order(request):
    order_serializer = OrderSerializer(data=request.data)
    order_serializer.is_valid(
        raise_exception=True)
    validated_order = order_serializer.validated_data
    new_order = Order.objects.create(
        firstname=validated_order['firstname'],
        lastname=validated_order['lastname'],
        phonenumber=validated_order['phonenumber'],
        address=validated_order['address'])
    order_items = [
        OrderItem(
            product_id=product['product'].id,
            quantity=product['quantity'],
            order=new_order
        )
        for product in validated_order['products']
    ]
    OrderItem.objects.bulk_create(order_items)
    serializer = OrderSerializer(new_order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
