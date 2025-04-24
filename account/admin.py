"""
This module contains the admin interface configuration for the Account model.

It registers the `Account` model in the Django admin site,\
    providing a custom interface for managing user-related data.
The `AccountAdmin` class customizes the display of fields,\
    search functionality, and permissions for the user records.
"""


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


class AccountAdmin(UserAdmin):
    """
    Custom admin interface for the `Account` model.

    This class customizes how the `Account` model is displayed \
        and interacted with in the Django admin panel.
    It includes customizations like:
    - Displaying fields like name, email, and account status in the list view.
    - Adding filters and search functionality for efficient user management.
    - Custom fieldsets for organizing user data into sections.
    - Managing user creation through the `add_fieldsets` option.

    Attributes:
        list_display (tuple): Fields displayed in the list view of the admin\
            interface.
        list_filter (tuple): Filters available in the sidebar to narrow\
            down the user list.
        search_fields (tuple): Fields searchable in the admin search bar.
        ordering (tuple): Default ordering of user entries in the\
            admin interface.
        fieldsets (tuple): Custom organization of the fields into sections\
            for the user detail view.
        add_fieldsets (tuple): Custom fields used when creating a new user.
        filter_horizontal (tuple): Empty because we don’t have any\
            ManyToMany relationships.
        readonly_fields (tuple): Fields that cannot be edited\
            in the admin interface.
    """

    # Defines the columns shown in the list view for `Account`
    # in the admin interface.
    list_display = (
        'first_name', 'last_name', 'email', 'phone_number',
        'is_staff', 'is_active'
    )

    # Defines the filters shown in the admin sidebar to filter users by
    # `is_staff` and `is_active` status.
    list_filter = ('is_staff', 'is_active')

    # Specifies the fields that can be searched via the admin search bar.
    # In this case, users can search by `email`, `first_name`, or `last_name`.
    search_fields = ('email', 'first_name', 'last_name')

    # Defines the default ordering of `Account` records
    # in the list view by `email`.
    ordering = ('email',)

    # Organizes the fields into sections for the user detail view
    # in the admin interface.
    fieldsets = (
        ("Personal Information", {
            "fields": (
                "first_name", "last_name", "email", "phone_number",
                "date_of_birth"
            )
        }),
        ("Permissions", {
            "fields": (
                "is_active", "is_staff", "is_superuser"
            )
        }),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    # Customizes the form for adding new users.
    # Defines the fields required during user creation.
    add_fieldsets = (
        ("Create New User", {
            "classes": ("wide",),
            "fields": (
                "email", "first_name", "last_name",
                "phone_number", "password1", "password2"
            ),
        }),
    )

    # No many-to-many relationships are defined, so this option is left empty.
    filter_horizontal = ()

    # Defines fields that should be displayed as read-only in the admin
    # interface, including `last_login` and `date_joined`.
    readonly_fields = ('last_login', 'date_joined')


# Registers the `Account` model with the custom `AccountAdmin`
# interface in the Django admin site.
admin.site.register(Account, AccountAdmin)
