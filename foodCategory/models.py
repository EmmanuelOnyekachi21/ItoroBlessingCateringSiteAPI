"""
Model definition for food categories used in the site.
Each category includes a name, slug, optional image, and description.
"""

from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """
    Represents a food category (e.g. main dishes, desserts)
    used to organize items in the system.
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(
        upload_to='category_images/', blank=True, null=True
    )
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Automatically generates a unique slug if not provided,
        or if the name changes during updates.
        """
        slug_value = self.slug
        if not slug_value:
            slug_value = slugify(self.name)
        elif self.id:
            original = Category.objects.get(id=self.id)
            if original.name != self.name:
                slug_value = slugify(self.name)

        base_slug = slug_value
        counter = 1
        while Category.objects.filter(
            slug=slug_value
        ).exclude(id=self.id).exists():
            slug_value = f'{base_slug}-{counter}'
            counter += 1

        self.slug = slug_value
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        indexes = [
            models.Index(fields=['slug'])
        ]
