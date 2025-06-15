"""
cart.models
-----------
Defines models for the shopping cart and cart items in the catering site API.
"""

from django.db import models
import uuid
from django.conf import settings
from dish.models import Dish, ExtraItem


class Cart(models.Model):
    """
    Represents a shopping cart for a user, containing order details and status.
    """
    ORDER_TYPES = (
        ('pickup', 'Pickup'),
        ('delivery', 'Delivery'),
    )
    cart_code = models.UUIDField(
        unique=True, null=False, default=uuid.uuid4, editable=False
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    order_type = models.CharField(
        choices=ORDER_TYPES, default='delivery', max_length=10
    )
    special_instruction = models.TextField(null=True)

    def __str__(self):
        """
        Returns a string representation of the cart,\
            showing the user and status
        """
        return (
            f'Cart for {self.user.email if self.user else "User"} - '
            f'{"Active" if self.is_active else "Completed"}'
        )


class CartItem(models.Model):
    """
    Represents an item in a cart, including dish, quantity, and extras.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    dish = models.ForeignKey(Dish, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=1)
    extras = models.ManyToManyField(
        ExtraItem,
        through='CartItemExtra',
        through_fields=('cart_item', 'extra'),
        blank=True
    )

    
    def __str__(self):
        """
        Returns a string representation of the cart item,\
            showing quantity and dish.
        """
        return (
            f"{self.quantity} x {self.dish.name} (Cart: {self.cart.cart_code})"
        )

class CartItemExtra(models.Model):
    """
    Represents an extra item added to a cart item within the shopping cart.
    Attributes:
        cart_item (ForeignKey): Reference to the CartItem this\
            extra is associated with.
        extra (ForeignKey): Reference to the ExtraItem being added.
        quantity (IntegerField): The number of this extra item\
            added to the cart item.
    Methods:
        __str__(): Returns a human-readable string representation\
            of the CartItemExtra instance.
    """
    
    cart_item = models.ForeignKey(
        CartItem, related_name='extra_items', on_delete=models.CASCADE
    )
    extra = models.ForeignKey(
        ExtraItem,
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        """
        Returns a short string with quantity, extra name, and cart code.
        """
        if not self.extra:
            return (
                f"{self.quantity} x Extra (No Name) "
                f"(Cart: {self.cart_item.cart.cart_code})"
            )
        return (
            f"{self.quantity} x {self.extra.name} "
            f"(Cart Item: {self.cart_item.cart.cart_code})"
        )

