"""
Models for managing individual dishes and related entities on the food site.

This module defines the following models:
- ExtraCategory: Represents a category for extra items that can be\
    added to dishes
- ExtraItem: Represents an individual extra item, linked to an ExtraCategory.
- Dish: Represents a food item listed on the platform,
    including metadata such as name, slug, description, price, availability,
    timestamps, and the category it belongs to.
    Also supports suggested pairings, allowed extras, and image uploads.

Each model includes relevant fields and string representations.
The Dish model auto-generates\
    a slug from the name if not provided.
"""

from django.db import models
from django.utils.text import slugify
from foodCategory.models import Category


class ExtraCategory(models.Model):
    """
    Represents a category for extra items that can be associated with dishes.
    Attributes:
        name (CharField): The name of the extra category.
    Meta:
        db_table (str): The name of the database table to use for the model.
        managed (bool): Whether the model is managed by Django's migrations.
        verbose_name (str): Human-readable singular name for the model.
        verbose_name_plural (str): Human-readable plural name for the model.
    """

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'ExtraCategory'
        verbose_name_plural = 'ExtraCategories'


class ExtraItem(models.Model):
    """
    Represents an extra item that can be added to a dish,
    such as toppings or sides.
    Attributes:
        name (str): The name of the extra item.
        price (Decimal): The price of the extra item.
        category (ExtraCategory): The category this extra item belongs to.
        is_available (bool): Indicates whether the extra item is currently\
            available.
    """
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(
        ExtraCategory, on_delete=models.CASCADE, related_name="extras"
    )
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Dish(models.Model):
    """
    This model is used to store and manage information about individual
    dishes offered on the food platform, including their details, pricing,
    availability, and relationships to categories, extras, and suggested
    pairings.

    Attributes:
        name (CharField): The unique name of the dish (max 100 characters).
        slug (SlugField): A unique, URL-friendly identifier for the dish,
            auto-generated from the name if not provided.
        price (DecimalField): The price of the dish, supporting up to 10
            digits and 2 decimal places.
        suggested_pairings (ManyToManyField): A set of other Dish instances
            that pair well with this dish.
        image (ImageField): An optional image representing the dish, uploaded
            to 'dish/image/'.
        category (ForeignKey): The category to which the dish belongs,
            referencing the Category model.
        is_available (BooleanField): Indicates whether the dish is currently
            available for order.
        allowed_extras (ManyToManyField): ExtraCategory instances that can be
            added to this dish.
    Methods:
        save(*args, **kwargs): Overrides the default save method to
            auto-generate a slug from the dish name if not provided.
        __str__(): Returns the string representation of the dish, which is its
            name.
    Meta:
        verbose_name_plural (str): The plural name for the model in the admin
            interface is set to 'Dishes'.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    suggested_pairings = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True
    )
    image = models.ImageField(
        upload_to='dish/image/', null=False, blank=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products'
    )
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    allowed_extras = models.ManyToManyField(
        ExtraCategory, blank=True, related_name='dishes'
    )

    def save(self, *args, **kwargs):
        """
        Auto-generates a slug from the dish name if not already provided.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Dishes'

    def __str__(self):
        return self.name
