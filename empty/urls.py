import logging

from django.conf import settings
from django.urls import path, include, re_path

from empty import views #change this

logger = logging.getLogger(__name__)

auto = True
app_name = 'empty' #change this
urlpatterns = [
    path('api/', include('empty.apis.urls'), name='empty'), #change this
]
