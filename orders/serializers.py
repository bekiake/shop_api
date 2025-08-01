from rest_framework import serializers
from orders.models import Order, OrderItem
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'created_at', 'items']

class OrderCreateSerializer(serializers.Serializer):
    confirm = serializers.BooleanField()  # tasdiqlash uchun


class OrderStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=['processing', 'shipped', 'delivered'])
