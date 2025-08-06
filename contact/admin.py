"""
Admin configuration for the Contact model in the Django admin interface.

This module registers the Contact model with custom display options, including:
- Displaying key fields such as name, email, phone number, subject,
    a shortened message, and creation date.
- Enabling search functionality on email and phone number fields.
- Adding a filter for the creation date.
- Providing a method to display a truncated version of the message
    for easier viewing in the admin list.

Author: [Your Name]
"""
from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Contact model.
    Displays the following fields in the list view: name, email, phone number,
    subject, a shortened version of the message, and creation date.
    Enables search functionality for email and phone number fields.
    Allows filtering by creation date.
    Includes a custom method 'short_message' to display the first 50
    characters of the message.
    """
    list_display = (
        'name',
        'email',
        'phone_number',
        'subject',
        'short_message',
        'created_at'
    )
    search_fields = (
        'email',
        'phone_number'
    )
    list_filter = ['created_at']

    def short_message(self, obj):
        """
        Returns a shortened version of the message attribute from the given
        object,
        limited to the first 50 characters followed by ellipsis.
        Args:
            obj: The object containing the 'message' attribute.
        Returns:
            str: A truncated message string ending with '...'.
        """
        return f'{obj.message[:50]}...'
    short_message.short_description = 'Message'
