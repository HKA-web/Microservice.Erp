import logging

from django.urls import path, include
from rest_framework import routers

from empty.apis import views

logger = logging.getLogger(__name__)

router = routers.DefaultRouter()
router.register(r'empty', views.EmptyViewSet, basename='empty')

app_name = 'api'
urlpatterns = [
    path('', include(router.urls), name='api'),
]
