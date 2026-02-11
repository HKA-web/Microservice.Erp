from django.contrib import admin
from chatterbot.ext.django.model_admin import StatementAdmin, TagAdmin
from chatterbot.ext.django.models import Statement, Tag


admin.site.register(Statement, StatementAdmin)
admin.site.register(Tag, TagAdmin)
