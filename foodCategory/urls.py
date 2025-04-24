"""
URL routing for the Category app.
Maps endpoint paths to category views.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.category_list_create, name='category-list')
]
