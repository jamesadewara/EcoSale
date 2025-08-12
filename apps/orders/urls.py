from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register(r'', OrderViewSet)

urlpatterns = [
    path('<uuid:pk>/cancel/', OrderViewSet.as_view({'post': 'cancel'}), name='order-cancel'),
    path('<uuid:pk>/confirm/', OrderViewSet.as_view({'post': 'confirm'}), name='order-confirm'),
    path('<uuid:pk>/ship/', OrderViewSet.as_view({'post': 'ship'}), name='order-ship'),
    path('<uuid:pk>/deliver/', OrderViewSet.as_view({'post': 'deliver'}), name='order-deliver'),
] + router.urls