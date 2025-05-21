"""
URL configuration for the bookings app.

This module defines the URL patterns for booking-related API endpoints.
It maps HTTP requests to the corresponding views for creating bookings.

Endpoints:
    - 'create/' (POST): Create a new booking.
    - 'get-booking-events/' (GET): Get all event types.
"""
from django.urls import path
from .views import create_booking, get_booking_choices

urlpatterns = [
    path('create/', create_booking, name='create-booking'),
    path('get-booking-events/', get_booking_choices, name='booking-events'),
]
