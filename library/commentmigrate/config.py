from django.conf import settings


class DCMConfig:
    defaults = {
        'COMMENT_MIGRATE_KEY': 'help_text',
        'COMMENT_MIGRATE_TABLE_KEY': 'verbose_name',
        'COMMENT_MIGRATE_BACKEND': None,
        'COMMENT_MIGRATE_EXCLUDE_MODEL': [],
    }

    def __getattr__(self, name):
        if name in self.defaults:
            return getattr(settings, name, self.defaults[name])


dcm_config = DCMConfig()
