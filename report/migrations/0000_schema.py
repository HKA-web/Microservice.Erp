from django.db import migrations

from report import settings


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    setup_database_sql = f'''
        CREATE SCHEMA IF NOT EXISTS {settings.SCHEMA};
    '''
    reverse_setup_database_sql = f'''
        DROP SCHEMA IF EXISTS {settings.SCHEMA} CASCADE;
    '''
    operations = [
        migrations.RunSQL(
            sql=setup_database_sql,
            reverse_sql=reverse_setup_database_sql
        )
    ]
