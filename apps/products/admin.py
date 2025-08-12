from django.contrib import admin
from .models import Product, Category, ProductImage, RecentlyViewed

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'price', 'category', 'is_active', 'is_deal')
    list_filter = ('category', 'is_active', 'is_deal')
    search_fields = ('title', 'description')
    inlines = [ProductImageInline]
    raw_id_fields = ('seller',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(RecentlyViewed)