from core.apis.datetime import DateTimeModelSerializer
from report.models import Schema, SchemaField
from library.restframeworkflexfields import FlexFieldsModelSerializer


class ModelSchemaSerializer(FlexFieldsModelSerializer, DateTimeModelSerializer, ):
    class Meta:
        model = Schema
        fields = [
            'schema_id',
            'schema_name',
            'database',
            'managed',
            'table_name',
            'query',
            'fields',
            'created',
            'modified',
            'read_only',
            'enable',
            'properties',
            'description',
        ]
        extra_kwargs = {
            'schema_id': {'required': False, },
            'table_name': {'required': False, },
            'query': {'required': False, },
            'fields': {'required': False, },
        }
        expandable_fields = {
            'fields': (
                'report.apis.serializers.FieldSchemaSerializer', {'many': True, },
            ),
        }

class FieldSchemaSerializer(FlexFieldsModelSerializer, DateTimeModelSerializer, ):
    class Meta:
        model = SchemaField
        fields = [
            'schema_field_id',
            'schema_field_name',
            'schema',
            'class_name',
            'kwargs',
        ]
        extra_kwargs = {
            'schema_field_id': {'required': False, },
        }
        expandable_fields = {
            'model_schema': (
                'report.apis.serializers.ModelSchemaSerializer', {'many': False, },
            ),
        }
