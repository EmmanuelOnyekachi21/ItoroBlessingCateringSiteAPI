"""
Models for managing individual dishes on the food site.

This module defines the Dish model, which represents a food item
listed on the platform. It includes metadata such as name, slug,
description, price, availability, timestamps, and the category
it belongs to.
"""

from django.db import models
from django.utils.text import slugify
from foodCategory.models import Category


class ExtraCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'ExtraCategory'
        verbose_name_plural = 'ExtraCategories'


class ExtraItem(models.Model):
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
    Represents a dish available for order on the food platform.
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

