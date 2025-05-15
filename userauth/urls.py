from django.urls import path
from userauth.views import register_view, login_view, logout_view, token_refresh_view

urlpatterns = [
    path('register/', register_view, name='register-view'),
    path('login/', login_view, name='login-view'),
    path('logout/', logout_view, name='logout-view'),
    path('refresh/', token_refresh_view, name='token-refresh-view'),
]
