from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet

router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = [
    # Include router-generated URLs
    path('', include(router.urls)),

    # Custom actions (if you still want them separately accessible)
    path('cart/add_item/', CartViewSet.as_view({'post': 'add_item'}), name='cart-add-item'),
    path('cart/remove_item/', CartViewSet.as_view({'post': 'remove_item'}), name='cart-remove-item'),
    path('cart/checkout/', CartViewSet.as_view({'post': 'checkout'}), name='cart-checkout'),
]
