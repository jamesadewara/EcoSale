from django.contrib import admin
from .models import Wishlist

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'products_count', 'created_at', 'updated_at')
    search_fields = ('user__email',)
    filter_horizontal = ('products',)
    
    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Products'

admin.site.register(Wishlist, WishlistAdmin)