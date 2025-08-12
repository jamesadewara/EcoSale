from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Wishlist
from .serializers import WishlistSerializer
from apps.products.models import Product
from apps.users.permissions import IsBuyer

class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [IsBuyer]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(wishlist)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if Wishlist.objects.filter(user=request.user).exists():
            return Response(
                {'error': 'Wishlist already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def add_product(self, request):
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        
        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        if wishlist.products.filter(id=product_id).exists():
            return Response(
                {'error': 'Product already in wishlist'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        wishlist.products.add(product)
        return Response({'status': 'product added to wishlist'})

    @action(detail=False, methods=['post'])
    def remove_product(self, request):
        wishlist = Wishlist.objects.get(user=request.user)
        product_id = request.data.get('product_id')
        
        try:
            product = Product.objects.get(id=product_id)
            wishlist.products.remove(product)
            return Response({'status': 'product removed from wishlist'})
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )