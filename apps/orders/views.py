from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer, OrderDetailSerializer
from apps.users.permissions import IsBuyerOrSeller, IsBuyer, IsSeller

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsBuyerOrSeller]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [IsBuyer()]
        elif self.action in ['confirm', 'ship', 'deliver']:
            return [IsSeller()]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'buyer':
            return self.queryset.filter(buyer=user)
        return self.queryset.filter(seller=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(buyer=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status not in ['pending', 'cancelled']:
            return Response(
                {'error': 'Cannot delete order in current status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status not in ['delivered', 'cancelled']:
            order.status = 'cancelled'
            order.save()
            return Response({'status': 'order cancelled'})
        return Response(
            {'error': 'Order cannot be cancelled'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        order = self.get_object()
        if order.status == 'pending':
            order.status = 'confirmed'
            order.save()
            return Response({'status': 'order confirmed'})
        return Response(
            {'error': 'Order cannot be confirmed'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def ship(self, request, pk=None):
        order = self.get_object()
        if order.status == 'confirmed':
            order.status = 'shipped'
            order.save()
            return Response({'status': 'order shipped'})
        return Response(
            {'error': 'Order cannot be shipped'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def deliver(self, request, pk=None):
        order = self.get_object()
        if order.status == 'shipped':
            order.status = 'delivered'
            order.save()
            return Response({'status': 'order delivered'})
        return Response(
            {'error': 'Order cannot be delivered'},
            status=status.HTTP_400_BAD_REQUEST
        )