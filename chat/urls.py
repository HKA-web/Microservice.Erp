from django.urls import path

from . import views

app_name = 'chat'
urlpatterns = [
    path('', views.indexs, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path('<str:room_name>/test/<str:message>', views.room_test, name='room_test'),
]
