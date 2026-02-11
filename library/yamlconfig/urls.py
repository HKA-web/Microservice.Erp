"""
URL mappings to display the YAMLCONF settings.  This should only be used
for admin users.  The views are protected via

    @login_required(login_url='/admin/login/')

If you have a special environment, you might need to adjust this.
"""
from django.urls import path, re_path
from yamlconfig import views

app_name = 'yamlconfig'
urlpatterns = [
    path('', views.index, name='index'),
    re_path('^(?P<name>.+)/$', views.attr_info, name='attr'),
]
