from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('tracking_id', 'buyer', 'seller', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('tracking_id', 'buyer__email', 'seller__email')
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)