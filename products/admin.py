from django.contrib import admin
from .models import Product, Category, Wishlist, ProductReview


class ProductReviewProductAdminInLine(admin.TabularInline):
    model = ProductReview


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class ProductReviewAdmin(admin.ModelAdmin):
    readonly_fields = (
        'user',
        'product',
        'stars',
        'content',
    )

    list_display = (
        'product',
        'stars',
        'content',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist)
