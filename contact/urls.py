"""
URL configuration for the contact app.

Defines routes for submitting contact messages.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.submit_contact_message, name="submit_contact")
]
