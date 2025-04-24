"""
Admin configuration for the Category model used in the food site.
Customizes how categories are displayed, filtered, and managed
within the Django admin interface.
"""


from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface options for the Category model.
    Controls listing, filtering, and editing behavior in the admin panel.
    """
    list_display = (
        'name', 'slug', 'created_at', 'updated_at', 'is_active'
    )
    list_filter = ('is_active', 'created_at')
    prepopulated_fields = {'slug': ("name",)}
    search_fields = ('name', 'slug')
    ordering = ('-created_at',)

    fieldsets = (
        ("Category Information", {
            "fields": ('name', 'slug', 'description', 'image', 'is_active')
        }),
        ("Timestamps", {
            "fields": ('created_at', 'updated_at'),
            "classes": ('collapse',)
        }),
    )

    add_fieldsets = (
        ("Category Information", {
            "classes": ("wide",),
            "fields": ('name', 'slug', 'description', 'image', 'is_active')
        }),
    )

    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Category, CategoryAdmin)
