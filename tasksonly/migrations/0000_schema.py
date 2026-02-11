from django.db import migrations


class Migration(migrations.Migration):
    initial = True

    dependencies = []
    setup_database_sql = """
            CREATE SCHEMA IF NOT EXISTS core;
            CREATE SCHEMA IF NOT EXISTS history;
        """

    reverse_setup_database_sql = """
            DROP SCHEMA IF EXISTS core CASCADE;
            DROP SCHEMA IF EXISTS history CASCADE;
        """  # noqa

    operations = [
        migrations.RunSQL(
            sql=setup_database_sql,
            reverse_sql=reverse_setup_database_sql
        )
    ]
