from django.contrib import admin

# Register your models here.
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'cart_code',
        'get_user_email',
        'is_active', 'paid',
    )
    search_fields = (
        'cart_code',
    )
    list_filter = (
        'is_active',
        'paid'
    )

    def get_user_email(self, obj):
        return obj.user.email if obj.user else 'Anonymous'
    get_user_email.short_description = 'User Email'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'dish', 'quantity', 'extras')
    search_fields = ('cart__cart_code', 'dish__name')
