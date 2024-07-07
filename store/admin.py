from django.contrib import admin
from django.db.models import Count
from django.db.models.query import QuerySet

from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', "Low")
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, category):
        return category.products_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory']
    list_editable = ['unit_price', 'inventory']
    list_per_page = 10
    list_filter = ['updated_at', InventoryFilter]
    search_fields = ['title']


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']
    list_per_page = 10
    search_fields = ['first_name', 'last_name']


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['city', 'full_address', 'customer']


class CartItemInline(admin.TabularInline):
    model = models.CartItem
    extra = 0


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['customer', 'created_at']
    ordering = ['-created_at']
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'created_at', 'payment_status']
    ordering = ['-modified_at']
    inlines = [OrderItemInline]


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'customer', 'product']
    ordering = ['-created_at']
