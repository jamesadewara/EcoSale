from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'', ProductViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('deals/', ProductViewSet.as_view({'get': 'deals'}), name='product-deals'),
    path('recent/', ProductViewSet.as_view({'get': 'recent'}), name='recent-products'),
] + router.urls