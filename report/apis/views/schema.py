import json

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.apis.permissions import ModelPermissionsExtra, IsAdminOrNotReadOnly
from core.apis.viewsets import DevExtremeModelViewSet
from report.apis.serializers import ModelSchemaSerializer, FieldSchemaSerializer
from report.models import Schema, SchemaField


class ModelSchemaViewSet(DevExtremeModelViewSet, ):
    permission_classes = [IsAdminOrNotReadOnly, ModelPermissionsExtra, ]
    extra_permissions = {}
    serializer_class = ModelSchemaSerializer
    queryset = Schema.objects.all()

    @action(
        detail=False,
        url_path='exists',
        url_name='exists',
        methods=['post'],
        permission_classes=[IsAuthenticated, ]
    )
    def exists(self, request, ):
        if 'model_schema_id' in request.data:
            return Response(
                Schema.objects
                .filter(**request.query_params.dict())
                .exclude(pk=request.data['model_schema_id'])
                .exists(),
                status=status.HTTP_200_OK, )
        else:
            return Response(
                Schema.objects
                .filter(**request.query_params.dict())
                .exists(),
                status=status.HTTP_200_OK, )

    @action(
        detail=False,
        url_path='delete',
        url_name='delete',
        methods=['post'],
        permission_classes=[IsAdminOrNotReadOnly, ModelPermissionsExtra, ]
    )
    def delete(self, request, *args, **kwargs):
        data = request.data.dict()
        values = json.loads(data['key'])
        if isinstance(values, list):
            model_schemas = Schema.objects.filter(pk__in=[model_schema['model_schema_id'] for model_schema in values])
            for model_schema in model_schemas:
                model_schema.delete()
            return Response(dict(
                message=_('ModelSchema data %(count)s have been successfully deleted') % dict(count=model_schemas.count()),
            ), status=status.HTTP_200_OK, )
        else:
            model_schema = Schema.objects.get(pk=values['model_schema_id'])
            model_schema.delete()
        return Response(dict(
            message=_('ModelSchema %(model_schema_name)s have been successfully deleted') % dict(model_schema_name=model_schema.schema_name),
        ), status=status.HTTP_200_OK, )


class FieldSchemaViewSet(DevExtremeModelViewSet, ):
    permission_classes = [IsAdminOrNotReadOnly, ModelPermissionsExtra, ]
    extra_permissions = {}
    serializer_class = FieldSchemaSerializer
    queryset = SchemaField.objects.all()

    @action(
        detail=False,
        url_path='exists',
        url_name='exists',
        methods=['post'],
        permission_classes=[IsAuthenticated, ]
    )
    def exists(self, request, ):
        if ('schema_field_id' in request.data):
            return Response(
                SchemaField.objects
                .filter(**request.query_params.dict())
                .exclude(pk=request.data['schema_field_id'])
                .exists(),
                status=status.HTTP_200_OK, )
        else:
            return Response(
                SchemaField.objects
                .filter(**request.query_params.dict())
                .exists(),
                status=status.HTTP_200_OK, )

    @action(
        detail=False,
        url_path='delete',
        url_name='delete',
        methods=['post'],
        permission_classes=[IsAdminOrNotReadOnly, ModelPermissionsExtra, ]
    )
    def delete(self, request, *args, **kwargs):
        data = request.data.dict()
        values = json.loads(data['key'])
        if isinstance(values, list):
            schema_fields = SchemaField.objects.filter(pk__in=[schema_field['schema_field_id'] for schema_field in values])
            for schema_field in schema_fields:
                schema_field.delete()
            return Response(dict(
                message=_('SchemaField data %(count)s have been successfully deleted') % dict(count=schema_fields.count()),
            ), status=status.HTTP_200_OK, )
        else:
            schema_field = SchemaField.objects.get(pk=values['schema_field_id'])
            schema_field.delete()
        return Response(dict(
            message=_('FieldSchema %(schema_field_name)s have been successfully deleted') % dict(schema_field_name=schema_field.schema_field_name),
        ), status=status.HTTP_200_OK, )
