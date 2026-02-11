from rest_framework import viewsets, status, serializers
from rest_framework.response import Response

from core.apis.viewsets import DevExtremeModelViewSet
from report.apis.serializers import ModelSerializer, FieldSchemaSerializer
from report.apps import ApplicationConfig
from report.models import Schema, SchemaField


class ModelViewSet(DevExtremeModelViewSet, ):

    def generate(self):
        # self.kwargs.get('unique')
        auth_permission, created = Schema.objects.get_or_create(
            model_schema_id=self.kwargs.get('unique'),
            defaults=dict(
                model_schema_id=self.kwargs.get('unique'),
                model_schema_name='Kontol',
                query='''
                select
                    a.name,
                    a.content_type_id,
                    a.codename,
                    b.app_label,
                    b.model
                from auth_permission a
                left outer join django_content_type b on b.id = a.content_type_id
                ''',
            ),
        )
        # id, created = FieldSchema.objects.get_or_create(
        #     schema_field_name='id',
        #     class_name='django.db.models.IntegerField',
        #     model_schema=auth_permission,
        #     kwargs=dict(primary_key=True, )
        # )
        codename, created = SchemaField.objects.get_or_create(
            schema_field_name='codename',
            class_name='django.db.models.CharField',
            model_schema=auth_permission,
            kwargs={'max_length': 100}
        )
        app_label, created = SchemaField.objects.get_or_create(
            schema_field_name='app_label',
            class_name='django.db.models.CharField',
            model_schema=auth_permission,
            kwargs={'max_length': 100}
        )
        model, created = SchemaField.objects.get_or_create(
            schema_field_name='model',
            class_name='django.db.models.CharField',
            model_schema=auth_permission,
            kwargs={'max_length': 100}
        )
        content_type_id, created = SchemaField.objects.get_or_create(
            schema_field_name='content_type_id',
            class_name='django.db.models.CharField',
            model_schema=auth_permission,
            kwargs={'max_length': 1000}
        )
        return auth_permission.as_model()

    @property
    def model(self):
        try:
            self.schema = Schema.objects.get(pk=self.kwargs.get('unique'))
        except:
            self.schema = Schema.objects.filter(model_schema_name=self.kwargs.get('unique')).first()
        if self.schema:
            return self.schema.as_model()
        raise serializers.ValidationError({
            'model': f'''Error model with unique {self.kwargs.get('unique')} not found''',
        })

    def get_queryset(self):
        return self.model.objects.all()

    def get_serializer_class(self):
        ModelSerializer.Meta.model = self.model
        ModelSerializer.Meta.fields = [
            field.name for field in ModelSerializer.Meta.model._meta.fields
        ]
        return ModelSerializer

    def list(self, request, *args, **kwargs):
        self.generate()
        data = super(ModelViewSet, self).list(request, *args, **kwargs).data
        return Response(dict(
            schema=FieldSchemaSerializer(self.schema.fields.all(), many=True).data,
            **data
        ))
