from django.urls import path, include

app_name = 'report'
urlpatterns = [

    path('api/', include('report.apis.urls'), name='report'),
]
