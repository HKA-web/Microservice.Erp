from django.contrib import auth
from rest_framework import serializers

from core.apis.datetime import DateTimeModelSerializer
from library.restframeworkflexfields import FlexFieldsModelSerializer


class ModelSerializer(FlexFieldsModelSerializer, DateTimeModelSerializer, ):
    class Meta:
        model = None
        fields = '__all__'
