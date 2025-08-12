from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WishlistViewSet

router = DefaultRouter()
router.register(r'wishlist', WishlistViewSet, basename='wishlist')

urlpatterns = [
    # Router-generated CRUD endpoints
    path('', include(router.urls)),

    # Custom wishlist actions
    path('wishlist/add_product/', WishlistViewSet.as_view({'post': 'add_product'}), name='wishlist-add-product'),
    path('wishlist/remove_product/', WishlistViewSet.as_view({'post': 'remove_product'}), name='wishlist-remove-product'),
]
