"""
Admin configuration for the Dish model.
"""

from django.contrib import admin
from .models import Dish


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    """
    Admin interface for managing dishes.
    """
    list_display = (
        'name', 'slug', 'price', 'is_available',
        'category', 'created_at', 'updated_at'
    )
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ('is_available', 'category', 'created_at')
    search_fields = ('name', 'slug', 'description')
    ordering = ('-updated_at',)

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ("Dish Information", {
            "fields": (
                'name', 'slug', 'description',
                'price', 'image', 'category', 'is_available'
            )
        }),
        ("Timestamps", {
            "fields": ('created_at', 'updated_at'),
            "classes": ('collapse',)
        }),
    )

    add_fieldsets = (
        ("Add New Dish", {
            "classes": ("wide",),
            "fields": (
                'name', 'slug', 'description',
                'price', 'image', 'category', 'is_available'
            ),
        }),
    )
