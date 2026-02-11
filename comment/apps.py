import logging
import sys
from datetime import datetime

import pytz
from django.apps import AppConfig, apps
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class ApplicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'comment'
    verbose_name = _('Comment')
    dependencies = [
        'authentication',
        'core',
    ]

    def ready(self):
        from core.utils import search
        from library.simplehistory.models import HistoricalChanges
        for model in [model for model in self.get_models() if HistoricalChanges.__name__.lower() not in (
            base.__name__.lower() for base in model.__bases__
        ) and not any(name in model.__name__.lower() for name in ['comment'])]:
            # search.register(model)
            pass
        pass
        from library.simplehistory.models import HistoricalChanges
        if not any(item in [
            'migrate',
            'makemigrations',
            'showmigrations',
            'cleanmigrations',
            'makemessages',
            'compilemessages',
            'makelocale',
            'compilelocale',
            'runredis',
            'dumpdata',
            'loaddata',
            'collectpermission',
        ] for item in sys.argv):
            logger.debug(f'Migration not detected, {self.name}.ready will Run')
            for model in [model for model in apps.get_models() if HistoricalChanges.__name__.lower() in (
                base.__name__.lower() for base in model.__bases__
            ) and not any(name in model.__name__.lower() for name in ['comment', ])]:
                def create_comment(sender, instance, created, **kwargs):
                    try:
                        from django.contrib.contenttypes.models import ContentType
                        from comment.models import Comment
                        if created:
                            if instance.prev_record:
                                fields = [field for field in instance.diff_against(instance.prev_record).changed_fields if not any(name in field for name in ['version', 'slug', 'password', 'token', 'properties', ])]
                                if len(fields) > 0:
                                    changeds = []
                                    for field in fields:
                                        changed = [f'{_(instance.instance_type._meta.get_field(field).verbose_name.lower().title())}', ':', ]
                                        value = getattr(instance.prev_record, field)

                                        def convert(data):
                                            if isinstance(data, datetime):
                                                data = data.replace(tzinfo=pytz.UTC, ).astimezone(timezone.get_current_timezone())
                                                data = data.strftime(str(_('%A, %d %b %Y, %H.%M.%S.{:03}'))).format(int(data.microsecond / 1000))
                                            return str(data)

                                        if value is not None:
                                            changed.append(convert(value))
                                        else:
                                            changed.append(str(_('Empty')))
                                        changed.append(str(_('to')))
                                        value = getattr(instance, field)
                                        changed.append(convert(value))
                                        changeds.append(' '.join(changed))
                                    Comment.objects.create(
                                        user=instance.history_user,
                                        content_type=ContentType.objects.get_for_model(instance.instance_type),
                                        object_id=instance.instance.pk,
                                        message=f'''{_('Changed')} {', '.join(changeds)}''',
                                        read_only=True,
                                    )
                            else:
                                value = (
                                    getattr(instance.instance, f'{instance.instance._meta.model_name.lower()}_name', None)
                                    or getattr(instance.instance, f'{instance.instance._meta.model_name.lower()}_title', None)
                                    or getattr(instance.instance, f'{instance.instance._meta.model_name.lower()}_label', None)
                                    or getattr(instance.instance, 'name', None)
                                    or getattr(instance.instance, 'title', None)
                                    or getattr(instance.instance, 'label', None)
                                    or instance.instance.pk
                                )
                                Comment.objects.create(
                                    user=instance.history_user,
                                    content_type=ContentType.objects.get_for_model(instance.instance_type),
                                    object_id=instance.instance.pk,
                                    message=f'''{_('Created')} {value}''',
                                    read_only=True,
                                )
                            logger.debug('Comment %s created', instance.instance._meta.model_name.lower())
                    except Exception as e:
                        logger.error(str(e))
                        return

                from django.db.models import signals
                signals.post_save.connect(
                    create_comment,
                    sender=model,
                    dispatch_uid=model.__name__.lower(),
                )
                logger.debug('Watch %s changed to auto create comment', model._meta.model_name.lower())
        __all__ = []
