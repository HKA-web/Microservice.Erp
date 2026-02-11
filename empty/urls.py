import logging
from django.urls import path, include, re_path
from empty import views

logger = logging.getLogger(__name__)

auto = True
app_name = 'empty'
urlpatterns = [
    re_path(r'^empty/$', views.EmptyView.as_view(), name='empty'),

    path('empty/', include('empty.apis.urls'), name='empty'),
]
