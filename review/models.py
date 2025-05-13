from django.db import models
from django.conf import settings
from dish.models import Dish
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1), MaxValueValidator(5)
        ]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} on {self.dish} ({self.rating}★)'

