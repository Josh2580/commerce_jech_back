# reviews/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ReviewViewSet

# Root router for reviews

router = DefaultRouter()
router.register('', ReviewViewSet, basename='reviews')



urlpatterns = [
    path('', include(router.urls)),
]





