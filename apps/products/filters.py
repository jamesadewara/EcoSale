import django_filters
from django.db import models
from .models import Product

class ProductFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='iexact')
    seller = django_filters.CharFilter(field_name='seller__email', lookup_expr='iexact')
    
    class Meta:
        model = Product
        fields = ['category', 'is_deal']
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(title__icontains=value) |
            models.Q(description__icontains=value)
        )

    @property
    def qs(self):
        queryset = super().qs
        sort_by = self.request.query_params.get('sort_by')
        
        if sort_by == 'price_asc':
            return queryset.order_by('price')
        elif sort_by == 'price_desc':
            return queryset.order_by('-price')
        elif sort_by == 'newest':
            return queryset.order_by('-created_at')
        elif sort_by == 'oldest':
            return queryset.order_by('created_at')
        return queryset