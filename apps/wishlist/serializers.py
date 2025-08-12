from rest_framework import serializers
from .models import Wishlist
from apps.products.serializers import ProductSerializer

class WishlistSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = Wishlist
        fields = ['id', 'products', 'created_at', 'updated_at']