import logging

from django.conf import settings
from django.urls import re_path

from comment import views

logger = logging.getLogger(__name__)

app_name = 'comment'
urlpatterns = [
    re_path(r'^comment/$', views.CommentView.as_view(), name='comment'),
    re_path(f'^comment/(?P<pk>[{settings.NUMBERING_PATTERN}]+)/$', views.CommentView.as_view(), name='comment'),
    re_path(f'^comment/(?P<pk>[{settings.NUMBERING_PATTERN}]+)/(?P<object>[{settings.NUMBERING_PATTERN}]+)/$', views.CommentView.as_view(), name='comment'),
    re_path(f'^comment/(?P<pk>[{settings.NUMBERING_PATTERN}]+)/(?P<object>[{settings.NUMBERING_PATTERN}]+)/(?P<offset>[{settings.NUMBERING_PATTERN}]+)/$', views.CommentView.as_view(), name='comment'),
    re_path(r'^flag/flag/$', views.CommentFlagView.as_view(), name='comment-flag'),
    re_path(r'^reaction/$', views.CommentReactionView.as_view(), name='comment-reaction'),
]
