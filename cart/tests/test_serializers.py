"""
cart.tests.test_serializers
=============================
Unit tests for cart app serializers.

This module contains pytest-based tests for the\
    CartSerializer and CartItemSerializer, ensuring correct serialization of \
        Cart and CartItem model instances, including related fields\
            such as user, dish, and extras.
"""
import pytest
from django.contrib.auth import get_user_model
from cart.models import *
from cart.serializers import *
from dish.models import Dish, ExtraItem, ExtraCategory
from foodCategory.models import Category
import uuid


User = get_user_model()


@pytest.fixture
def user():
    """
    Creates and returns a new User instance with a predefined email address.
    Returns:
        User: A newly created User object with the email 'test@example.com'.

    """
    return User.objects.create(
        email='test@example.com'
    )


@pytest.fixture
def category():
    """
    Creates and returns a new Category instance with the name 'Main dishes'.
    Returns:
        Category: The created Category object.
    """

    return Category.objects.create(
        name='Main dishes',
    )


@pytest.fixture
def dish(category):
    """
    Creates and returns a Dish instance with predefined attributes.
    Args:
        category: The category to which the dish belongs.
    Returns:
        Dish: The created Dish instance with:
            name 'Rice',
            price 100,
            description 'Do nce',
            and image 'png.jpg'.
    """
    return Dish.objects.create(
        name='Rice',
        category=category,
        price=100,
        description="Do nce",
        image="png.jpg"
    )


@pytest.fixture
def cart(user, cart_code=uuid.uuid4()):
    """
    Creates and returns a new Cart instance for the specified user.
    Args:
        user (User): The user to associate with the cart.
        cart_code (UUID, optional): The unique identifier for the cart.
    Returns:
        Cart: The created Cart instance.
    """
    return Cart.objects.create(user=user, cart_code=cart_code)


@pytest.fixture
def extra_category():
    """
    Creates and returns an ExtraCategory instance with the name 'toppings'.
    Returns:
        ExtraCategory: The created ExtraCategory object.
    """
    return ExtraCategory.objects.create(name="toppings")


@pytest.fixture
def extra(extra_category):
    """
    Creates and returns a list of ExtraItem instances\
        associated with the given extra_category.
    Args:
        extra_category (ExtraCategory): The category to associate with the\
            created ExtraItem instances.
    Returns:
        list: A list containing two ExtraItem objects\
            ("Extra Cheese" and "Olives") with specified prices.
    """
    extra1 = ExtraItem.objects.create(
        name="Extra Cheese", category=extra_category, price=1.50
    )
    extra2 = ExtraItem.objects.create(
        name="Olives", category=extra_category, price=1.00
    )
    extras = [extra1, extra2]
    return extras


@pytest.fixture
def cart_item(cart, dish, extra):
    """
    Creates a CartItem instance with the specified cart, dish, and extras.
    Args:
        cart (Cart): The cart to which the item will be added.
        dish (Dish): The dish to be added to the cart.
        extra (iterable): An iterable of extra items to associate with the\
            cart item.
    Returns:
        CartItem: The created CartItem instance with the\
            specified cart, dish, quantity, and extras set.
    """
    cartitem = CartItem.objects.create(
        cart=cart, dish=dish, quantity=2
    )
    cartitem.extras.set(extra)
    return cartitem


@pytest.mark.django_db
def test_cart_serializer(cart):
    """
    Test the CartSerializer to ensure it correctly serializes\
        the Cart instance.
    Args:
        cart: A Cart instance fixture to be serialized.
    Asserts:
        - The serialized 'cart_code' matches the Cart instance's cart_code\
            as a string.
        - The serialized 'user' matches the Cart instance's user as a string.
        - The serialized 'paid' status matches the Cart instance's paid\
            attribute.
    """
    serializer = CartSerializer(instance=cart)
    data = serializer.data
    assert data['cart_code'] == str(cart.cart_code)
    assert data['user'] == str(cart.user)
    assert data['paid'] == cart.paid


@pytest.mark.django_db
def test_cart_item_serializer(cart_item, cart, dish):
    """
    Test the CartItemSerializer to ensure it serializes cart item data\
        correctly.
    Args:
        cart_item: An instance of the CartItem model to be serialized.
        cart: The Cart instance associated with the cart item.
        dish: The Dish instance associated with the cart item.
    Asserts:
        - The serialized cart_code matches the cart's cart_code.
        - The serialized dish name matches the dish's name.
        - The serialized quantity is equal to 2.
    """
    serializer = CartItemSerializer(instance=cart_item)
    data = serializer.data
    assert data['cart']['cart_code'] == str(cart.cart_code)
    assert data['dish']['name'] == dish.name
    assert data['quantity'] == 2
