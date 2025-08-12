from rest_framework import serializers
from .models import Order, OrderItem
from apps.products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price_at_purchase']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['tracking_id', 'status', 'total_amount', 'created_at']

class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    buyer = serializers.SerializerMethodField()
    seller = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'tracking_id', 'status', 'total_amount', 'delivery_address',
            'created_at', 'updated_at', 'items', 'buyer', 'seller'
        ]
    
    def get_buyer(self, obj):
        from apps.users.serializers import UserProfileSerializer
        return UserProfileSerializer(obj.buyer).data
    
    def get_seller(self, obj):
        from apps.users.serializers import UserProfileSerializer
        return UserProfileSerializer(obj.seller).data