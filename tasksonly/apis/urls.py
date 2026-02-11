from django.urls import path, include
from rest_framework import routers

from empty.apis import views

router = routers.DefaultRouter()
router.register(r'empty', views.EmptyViewSet, basename='empty')

urlpatterns = [
    path('', include(router.urls), name='api.router'),
]
