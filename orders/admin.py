from django.contrib import admin
from .models import Food, Order


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'category',
        'price',
    )

    list_filter = (
        'category',
    )

    search_fields = (
        'name',
        'description',
    )

    ordering = (
        'name',
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'customer',
        'food',
        'quantity',
        'total_price',
        'status',
        'ordered_at',
    )

    list_filter = (
        'status',
        'ordered_at',
    )

    search_fields = (
        'customer__username',
        'customer_name',
        'phone',
        'food__name',
        'delivery_address',
    )

    ordering = (
        '-ordered_at',
    )

    list_per_page = 20