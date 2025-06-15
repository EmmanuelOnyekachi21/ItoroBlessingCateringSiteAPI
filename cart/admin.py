from django.contrib import admin

# Register your models here.
from .models import Cart, CartItem, CartItemExtra
from dish.models import ExtraItem


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


class CartItemExtraInline(admin.TabularInline):
    model = CartItemExtra
    extra = 1
    verbose_name = 'Extra Item'
    verbose_name_plural = 'Extra Items'
    autocomplete_fields = ('extra',)


@admin.register(ExtraItem)
class ExtraItemAdmin(admin.ModelAdmin):
    search_fields = ['name']  # 👈 this is what enables autocomplete


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'dish', 'quantity')
    search_fields = ('cart__cart_code', 'dish__name')
    inlines = (CartItemExtraInline,)

    fieldsets = (
        ("CartItem Information", {
            "fields": (
                'cart', 'dish', 'quantity'
            )
        }),
    )
    
    add_fieldsets = (
        ("Add CartItem", {
            "classes": ("wide",),
            'fields': ('cart', 'dish', 'quantity', 'extras'),
        }),
    )
