"""
Serializer for the Booking model.

This serializer handles conversion between Booking model instances and JSON
representations for API interactions. It includes all fields from the Booking
model, with 'booking_id' and 'date_submitted' set as read-only fields.

    booking_id (UUIDField): Unique identifier for the booking (read-only).
    date_submitted (DateTimeField): Timestamp when booking was submitted
        (read-only).

"""
from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model, converting model instances to and from
    JSON format.

    Fields:
        booking_id (UUIDField): Unique identifier for the booking.
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
        is_confirmed (BooleanField): Indicates if the booking is confirmed.
    """

    class Meta:
        model = Booking
        fields = '__all__'
    booking_id = serializers.UUIDField(
        read_only=True,
    )

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = (
            'user', 'booking_id', 'date_submitted',
            'is_pending', 'is_confirmed', 'is_declined'
        )
