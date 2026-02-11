from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.db.utils import DEFAULT_DB_ALIAS as DatabaseAlias
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from core.fields import ShortUUIDField
from core.models import Base, History, Tracker
from report import settings
from report.apps import ApplicationConfig
from report.exceptions import InvalidFieldNameError, NullFieldChangedError
from report.factory import ModelFactory
from report.fields import FieldKwargsJSON
from report.schema import FieldSchemaEditor, ModelSchemaEditor
from report.utils import ModelRegistry


class Schema(Base, ):
    schema_id = ShortUUIDField(
        length=25,
        primary_key=True,
        verbose_name=_('schema id'),
        help_text=_('Used for identity'),
    )
    schema_name = models.CharField(
        unique=True,
        verbose_name=_('schema name'),
        help_text=_('Used for view'),
    )
    database = models.CharField(
        default=DatabaseAlias,
        verbose_name=_('database'),
        help_text=_('Used for database alias'),
    )
    query = models.TextField(
        null=True,
        verbose_name=_('query'),
        help_text=_('Used for auto generate table view'),
    )
    tracker = Tracker()
    history = History(
        table_name=u'\"history".\"{}_schema\"'.format(settings.SCHEMA),
        verbose_name=_('Used store history schema'),
        excluded_fields=['modified', ],
    )

    class Meta:
        managed = True
        db_table = u'\"{}\".\"schema\"'.format(settings.SCHEMA)
        verbose_name = _('Used store schema')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._registry = ModelRegistry(self.app_label)
        self._initial_name = self.schema_name
        initial_model = self.get_registered_model()
        self._schema_editor = ModelSchemaEditor(
            initial_model=initial_model,
            query=self.query,
            database=self.database,
        )

    def save(self, **kwargs):
        super().save(**kwargs)
        self.fields.model.objects.get_or_create(
            schema_field_name='id',
            class_name='django.db.models.IntegerField',
            model_schema=self,
            kwargs=dict(primary_key=True, )
        )
        if self._schema_editor:
            self._schema_editor.update_table(self._factory.get_model())
        self._initial_name = self.schema_name

    def delete(self, **kwargs):
        if self._schema_editor:
            self._schema_editor.drop_table(self.as_model())
        self._factory.destroy_model()
        super().delete(**kwargs)

    def get_registered_model(self):
        return self._registry.get_model(self.model_name)

    @property
    def _factory(self):
        return ModelFactory(self)

    @property
    def app_label(self):
        return ApplicationConfig.name

    @property
    def model_name(self):
        return self.get_model_name(self.schema_name)

    @property
    def initial_model_name(self):
        return self.get_model_name(self._initial_name)

    @classmethod
    def get_model_name(cls, name):
        return name.title().replace(' ', '')

    @property
    def db_table(self):
        return self._default_table_name()

    def _default_table_name(self):
        safe_name = slugify(self.schema_name).replace('-', '_')
        return f'''\"{self.app_label}\".\"{safe_name}\"'''

    def as_model(self):
        return self._factory.get_model()


class SchemaField(Base, ):
    _PROHIBITED_NAMES = ('__module__', '_declared')
    schema_field_id = ShortUUIDField(
        length=25,
        primary_key=True,
        verbose_name=_('schema field id'),
        help_text=_('Used for identity'),
    )
    schema_field_name = models.CharField(
        verbose_name=_('schema field name'),
        help_text=_('Used for view'),
    )
    schema = models.ForeignKey(
        to=Schema,
        on_delete=models.CASCADE,
        related_name='fields',
        verbose_name=_('schema'),
        help_text=_('Used for linked key'),
    )
    class_name = models.CharField(
        verbose_name=_('class name'),
        help_text=_('Used for django field class'),
    )
    kwargs = FieldKwargsJSON(
        default=dict,
        verbose_name=_('kwargs'),
        help_text=_('Used for propertie field'),
    )
    tracker = Tracker()
    history = History(
        table_name=u'\"history".\"{}_schema_field\"'.format(settings.SCHEMA),
        verbose_name=_('Used store history schema field'),
        excluded_fields=['modified', ],
    )

    class Meta:
        managed = True
        db_table = u'\"{}\".\"schema_field\"'.format(settings.SCHEMA)
        unique_together = (('schema_field_name', 'schema',),)
        verbose_name = _('Used store schema field')
        ordering = ('schema_field_id',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initial_name = self.schema_field_name
        self._initial_null = self.null
        self._initial_field = self.get_registered_model_field()
        self._schema_editor = FieldSchemaEditor(
            initial_field=self._initial_field,
            query=self.schema.query,
            database=self.schema.database,
        )

    def save(self, **kwargs):
        self.validate()
        super().save(**kwargs)
        model, field = self._get_model_with_field()
        if self._schema_editor:
            self._schema_editor.update_column(model, field)

    def delete(self, **kwargs):
        model, field = self._get_model_with_field()
        if self._schema_editor:
            self._schema_editor.drop_column(model, field)
        super().delete(**kwargs)

    def validate(self):
        if self._initial_null and not self.null:
            raise NullFieldChangedError(f'''Cannot change NULL field '{self.schema_field_name}' to NOT NULL''')
        if self.schema_field_name in self.get_prohibited_names():
            raise InvalidFieldNameError(f'''{self.schema_field_name} is not a valid field name''')

    def get_registered_model_field(self):
        latest_model = self.schema.get_registered_model()
        if latest_model and self.schema_field_name:
            try:
                return latest_model._meta.get_field(self.schema_field_name)
            except FieldDoesNotExist:
                pass

    @classmethod
    def get_prohibited_names(cls):
        return cls._PROHIBITED_NAMES

    @property
    def db_column(self):
        return slugify(self.schema_field_name).replace('-', '_')

    @property
    def null(self):
        return self.kwargs.get('null', False)

    @null.setter
    def null(self, value):
        self.kwargs['null'] = value

    def get_options(self):
        return self.kwargs.copy()

    def _get_model_with_field(self):
        model = self.schema.as_model()
        try:
            field = model._meta.get_field(self.db_column)
        except FieldDoesNotExist:
            field = None
        return model, field
