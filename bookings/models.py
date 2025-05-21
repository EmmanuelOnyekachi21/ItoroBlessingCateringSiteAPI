"""
Models for handling event bookings in the Itoro Blessing Catering Site API.

This module defines the Booking model, which stores information about event
bookings, including customer details, event type, date, guest count, venue,
and additional requests.

Represents a booking for an event.

Fields:
    booking_id (UUIDField): Unique identifier for the booking.
    user (ForeignKey): Reference to the user who made the booking.
    full_name (CharField): Full name of the person making the booking.
    email (EmailField): Email address of the customer.
    phone_number (CharField): Contact phone number.
    event_type (CharField): Type of event (e.g., wedding, birthday, corporate, etc.).
    event_date (DateField): Date of the event.
    number_of_guests (PositiveIntegerField): Number of guests expected.
    venue_location (CharField): Location where the event will be held.
    special_requests (TextField): Any special requests from the customer (optional).
    additional_info (TextField): Additional information about the booking (optional).
    date_submitted (DateTimeField): Timestamp when the booking was submitted.
    is_pending (BooleanField): Indicates if the booking is pending.
    is_confirmed (BooleanField): Indicates if the booking has been confirmed.
    is_declined (BooleanField): Indicates if the booking has been declined.

Methods:
    __str__(): Returns a string representation of the booking.
"""
from django.db import models
import uuid
from django.conf import settings


class Booking(models.Model):
    """
    Represents a booking for an event, storing customer, user, and event details.

    Fields:
        booking_id (UUIDField): Unique identifier for the booking.
        user (ForeignKey): Reference to the user who made the booking.
        full_name (CharField): Full name of the person making the booking.
        email (EmailField): Email address of the customer.
        phone_number (CharField): Contact phone number.
        event_type (CharField): Type of event (e.g., wedding, birthday, etc.).
        event_date (DateField): Date of the event.
        number_of_guests (PositiveIntegerField): Number of expected guests.
        venue_location (CharField): Location where the event will be held.
        special_requests (TextField): Special requests from the customer.
        additional_info (TextField): Additional booking information (optional).
        date_submitted (DateTimeField): Timestamp when booking was submitted.
        is_pending (BooleanField): Indicates if the booking is pending.
        is_confirmed (BooleanField): Indicates if the booking is confirmed.
        is_declined (BooleanField): Indicates if the booking is declined.

    Methods:
        __str__(): Returns a string representation of the booking.
    """

    EVENT_TYPES = [
        ('wedding', 'Wedding Ceremony'),
        ('birthday', 'Birthday Party'),
        ('corporate', 'Corporate Event'),
        ('funeral', 'Funeral'),
        ('anniversary', 'Anniversary'),
        ('graduation', 'Graduation'),
        ('other', 'Other'),
    ]
    
    NUMBER_OF_GUEST = [
        ('under50', 'Under 50'),
        ('50-100', '50 - 100'),
        ('100-200', '100 - 200'),
        ('200-300', '200 - 300'),
        ('300+', '300+'),
    ]
    booking_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
        null=True,
        blank=True,
    )
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    event_type = models.CharField(
        max_length=50,
        choices=EVENT_TYPES,
    )
    event_date = models.DateField()
    number_of_guests = models.CharField(
        choices=NUMBER_OF_GUEST,
        max_length=50
    )
    venue_location = models.CharField(max_length=255)
    special_requests = models.TextField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    date_submitted = models.DateTimeField(auto_now_add=True)
    is_pending = models.BooleanField(default=True)
    is_confirmed = models.BooleanField(default=False)
    is_declined = models.BooleanField(default=False)

    def __str__(self):
        """
        Return a human-readable string representation of the booking instance,
        including the full name, event type, and event date
        """
        return f"Booking {self.booking_id} - {self.full_name}"
