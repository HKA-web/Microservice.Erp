from django.core.exceptions import ValidationError
from django.db import models

from report import compat


class FieldKwargsJSON(compat.JSONField):
    description = 'A field that handles storing models.Field kwargs as JSON'

    def to_python(self, value):
        raw_value = super().to_python(value)
        try:
            return self._convert_on_delete_to_function(raw_value)
        except AttributeError as err:
            raise ValidationError('''Invalid value for 'on_delete' ''') from err

    def from_db_value(self, value, expression, connection):
        try:
            db_value = super().from_db_value(value, expression, connection)
        except AttributeError:
            db_value = value
        return self._convert_on_delete_to_function(db_value)

    def get_prep_value(self, value):
        prep_value = self._convert_on_delete_to_string(value)
        return super().get_prep_value(prep_value)

    def _convert_on_delete_to_function(self, raw_value):
        if raw_value is None or 'on_delete' not in raw_value:
            return raw_value

        raw_on_delete = raw_value['on_delete']
        if isinstance(raw_on_delete, str):
            raw_value['on_delete'] = getattr(models, raw_on_delete)

        return raw_value

    def _convert_on_delete_to_string(self, raw_value):
        if raw_value is None or 'on_delete' not in raw_value:
            return raw_value

        raw_on_delete = raw_value['on_delete']
        if callable(raw_on_delete):
            raw_value['on_delete'] = raw_on_delete.__name__

        return raw_value
