from rest_framework import serializers
from .models import Product, ProductImage, Category

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'category', 'is_deal', 'deal_price', 'images']

class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    seller = serializers.SerializerMethodField()
    similar_products = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'price', 'category', 
            'stock_quantity', 'is_deal', 'deal_price', 'created_at',
            'seller', 'images', 'similar_products'
        ]
    
    def get_seller(self, obj):
        from apps.users.serializers import UserProfileSerializer
        return UserProfileSerializer(obj.seller).data
    
    def get_similar_products(self, obj):
        similar = Product.objects.filter(
            category=obj.category,
            is_active=True
        ).exclude(id=obj.id)[:4]
        return ProductSerializer(similar, many=True).data

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']