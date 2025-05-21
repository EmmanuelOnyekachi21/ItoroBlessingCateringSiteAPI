from django.urls import path
from userauth.views import (
    register_view, login_view, logout_view, token_refresh_view,
    verify_email_view, regenerate_token, request_password_reset_view,
    verify_password_reset_token_view
)

urlpatterns = [
    path('register/', register_view, name='register-view'),
    path('login/', login_view, name='login-view'),
    path('logout/', logout_view, name='logout-view'),
    path('refresh/', token_refresh_view, name='token-refresh-view'),
    path('verify/', verify_email_view, name='verify-email'),
    path('regenerate-token/', regenerate_token, name='regen-token'),
    path('reset-password/', request_password_reset_view, name='reset-password-view'),
    path('confirm-password-reset/', verify_password_reset_token_view, name='verify_pwd_reset'),
]
