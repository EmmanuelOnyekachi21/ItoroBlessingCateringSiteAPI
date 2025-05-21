"""
Admin configuration for the Booking model in the bookings app.

This module registers the Booking model with the Django admin site and
customizes its display, filtering, and search options for easier management.
"""
from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Booking model.
    This class customizes the Django admin panel for bookings by specifying:
    - Fields to display in the list view (`list_display`)
    - Filters available in the sidebar (`list_filter`)
    - Fields searchable via the search bar (`search_fields`)
    - Fields set as read-only in the admin form (`readonly_fields`)
    """
    list_display = (
        'booking_id',
        'full_name',
        'email',
        'phone_number',
        'event_type',
        'event_date',
        'number_of_guests',
        'venue_location',
        'is_pending',
        'is_confirmed',
        'is_declined',
        'date_submitted',
    )
    list_filter = ('event_type', 'is_confirmed', 'is_pending', 'is_declined', 'event_date')
    search_fields = ('full_name', 'email', 'phone_number', 'venue_location')
    readonly_fields = ('booking_id', 'date_submitted')