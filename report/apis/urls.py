from django.urls import path, include, re_path
from rest_framework import routers

from authentication.apis import views
from report.apis import views

router = routers.DefaultRouter()
router.register(r'modelschema', views.ModelSchemaViewSet, basename='modelschema')
router.register(r'fieldschema', views.FieldSchemaViewSet, basename='fieldschema')

app_name = 'api'
urlpatterns = [
    # : /report/api/general/application_name/model_name/?requireTotalCount=true
    re_path(r'^general/(?P<application>\w+)/(?P<model>\w+)', views.GeneralViewSet.as_view(dict(get='list')), name='general'),
    # : /report/api/model/unique/?requireTotalCount=true&skip=310&take=10
    re_path(r'^model/(?P<unique>\w+)', views.ModelViewSet.as_view(dict(get='list')), name='model'),
    path('', include(router.urls), name='api'),
]
