import pytest
from django.contrib.auth import get_user_model
from cart.models import *
from cart.serializers import *
from dish.models import Dish, ExtraItem
import uuid


User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create(
        email='test@example.com'
    )

@pytest.fixture
def dish():
    return Dish.objects.create(name='Rice', price=100, description="Do nce", image="png.jpg")


@pytest.fixture
def cart(user):
    return Cart.objects.create(user=user, cart_code=uuid.uuid4())


@pytest.fixture
def extra():
    extra1 = ExtraItem.objects.create(name="Extra Cheese", price=1.50)
    extra2 = ExtraItem.objects.create(name="Olives", price=1.00)
    extras = [extra1, extra2]
    return extras


@pytest.fixture
def cart_item(cart, dish, extra):
    cartitem = CartItem.objects.create(
        cart=cart, dish=dish, quantity=2, extras=extra
    )
    cartitem.extras.set(extra)
    return cartitem


@pytest.mark.django_db
def test_cart_serializer(cart):
    serializer = CartSerializer(instance=cart)
    data = serializer.data
    assert data['cart_code'] == str(cart.cart_code)
    assert data['user'] == str(cart.user)
    assert data['paid'] == cart.paid


# @pytest.mark.django_db
# def test_cart_item_serializer(cart_item, cart, dish):
#     serializer = CartItemSerializer(instance=cart_item)
#     data = serializer.data
#     assert data['cart']['cart_code'] == str(cart.cart_code)
#     assert data['dish']['name'] == dish.name
#     assert data['quantity'] == 2
