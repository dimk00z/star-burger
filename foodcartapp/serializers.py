from .models import Order, OrderItem, Product
from rest_framework.serializers import ModelSerializer, ValidationError


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderItemSerializer(many=True,
                                   required=True)

    class Meta:
        model = Order
        fields = '__all__'

    def validate_products(self, value):
        if not value:
            raise ValidationError("products can't be an empty list")
        return value
