from django.db import connections
from django.db.utils import DEFAULT_DB_ALIAS as DatabaseAlias, ProgrammingError


class ModelSchemaEditor:
    def __init__(self, initial_model=None, query=None, database=DatabaseAlias):
        self.initial_model = initial_model
        self.query = query
        self.database = database

    def update_table(self, new_model):
        if self.initial_model and self.initial_model != new_model:
            self.alter_table(new_model)
        elif not self.initial_model:
            self.create_table(new_model)
        self.initial_model = new_model

    def create_table(self, new_model):
        try:
            if self.query is None:
                with connections[self.database].schema_editor() as editor:
                    editor.create_model(new_model)
            else:
                with connections[self.database].cursor() as cursor:
                    cursor.execute(f'''CREATE OR REPLACE VIEW {new_model._meta.db_table} AS SELECT ROW_NUMBER () OVER() AS id, * FROM ( {self.query} ) AS queryset''')
                    connections[self.database].commit()
        except ProgrammingError:
            pass

    def alter_table(self, new_model):
        old_name = self.initial_model._meta.db_table
        new_name = new_model._meta.db_table
        if self.query is None:
            with connections[self.database].schema_editor() as editor:
                editor.alter_db_table(new_model, old_name, new_name)
        else:
            with connections[self.database].cursor() as cursor:
                cursor.execute(f'''DROP VIEW IF EXISTS {old_name}''')
                cursor.execute(f'''CREATE OR REPLACE VIEW {new_name} AS SELECT ROW_NUMBER () OVER() AS id, * FROM ( {self.query} ) AS queryset''')
                connections[self.database].commit()

    def drop_table(self, model):
        if self.query is None:
            with connections[self.database].schema_editor() as editor:
                editor.delete_model(model)
        with connections[self.database].cursor() as cursor:
            cursor.execute(f'''DROP VIEW IF EXISTS {model._meta.db_table}''')
            connections[self.database].commit()


class FieldSchemaEditor:
    def __init__(self, initial_field=None, query=None, database=DatabaseAlias):
        self.initial_field = initial_field
        self.query = query
        self.database = database

    def update_column(self, model, new_field):
        if self.initial_field and self.initial_field != new_field:
            self.alter_column(model, new_field)
        elif not self.initial_field:
            self.add_column(model, new_field)
        self.initial_field = new_field

    def add_column(self, model, field):
        if self.query is None:
            with connections[self.database].schema_editor() as editor:
                editor.add_field(model, field)

    def alter_column(self, model, new_field):
        if self.query is None:
            with connections[self.database].schema_editor() as editor:
                editor.alter_field(model, self.initial_field, new_field)

    def drop_column(self, model, field):
        if self.query is None:
            with connections[self.database].schema_editor() as editor:
                editor.remove_field(model, field)
