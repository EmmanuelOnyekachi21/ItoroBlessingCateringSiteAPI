from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'dish', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'dish')
    search_fields = ('user__username', 'dish__name', 'comment')
