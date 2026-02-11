import sys

from django.apps import AppConfig, apps
from django.contrib.auth import get_user_model
from django.db import DEFAULT_DB_ALIAS
from django.db.models.signals import post_migrate

from library.commentmigrate.config import dcm_config


def handle_post_migrate(app_config, using=DEFAULT_DB_ALIAS, **kwargs):
    from .db_comments import migrate_app_models_comment_to_database
    from .utils import get_migrations_app_models
    from django.contrib.auth.models import User

    migrations = (migration for migration, rollback in kwargs.get('plan', []) if not rollback)
    app_models = get_migrations_app_models(migrations, apps, using)
    if get_user_model() != User:
        app_models -= {User}
    exclude = []
    if (dcm_config.COMMENT_MIGRATE_EXCLUDE_MODEL and isinstance(dcm_config.COMMENT_MIGRATE_EXCLUDE_MODEL, list)):
        exclude = dcm_config.COMMENT_MIGRATE_EXCLUDE_MODEL
        exclude = [string.lower() for string in exclude]
    app_models = [app_model for app_model in app_models if app_model._meta.model.__name__.lower() not in exclude and app_model._meta.managed]
    migrate_app_models_comment_to_database(app_models, using)


class DjangoCommentMigrationConfig(AppConfig):
    name = 'commentmigrate'
    verbose_name = 'Comment Migrate'

    def ready(self) -> None:
        if any(item in [
            'migrate',
            'makemigrations',
            'showmigrations',
        ] for item in sys.argv):
            print('Migration detected, CommentMigrate.ready will Run')
            post_migrate.connect(handle_post_migrate)
        pass
