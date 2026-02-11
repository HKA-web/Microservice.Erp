import warnings

from django.conf import settings
from django.db import connections
from django.utils.module_loading import import_string

from commentmigrate.config import dcm_config


def get_migration_class_from_engine(engine):
    engine_name = engine.split('.')[-1]
    if (
        dcm_config.COMMENT_MIGRATE_BACKEND
        and isinstance(dcm_config.COMMENT_MIGRATE_BACKEND, dict)
        and dcm_config.COMMENT_MIGRATE_BACKEND.get(engine_name)
    ):
        path = dcm_config.COMMENT_MIGRATE_BACKEND.get(engine_name)
    else:
        if 'postgresql' in engine_name:
            engine_name = 'postgresql'
        path = f'commentmigrate.backends.{engine_name}.CommentMigration'
    return import_string(path)


def migrate_app_models_comment_to_database(app_models, using):
    engine = settings.DATABASES[using]['ENGINE']
    try:
        migration_class = get_migration_class_from_engine(engine)
    except ImportError:
        warnings.warn(
            f'{engine} is not supported by this comment migration' f' backend.'
        )
    else:
        for model in app_models:
            executor = migration_class(connection=connections[using], model=model)
            executor.execute()
