from django.core.management.base import BaseCommand

from permission.utils import clean_orphan_object_perms


class Command(BaseCommand):
    help = '''Removes object permissions with not existing targets'''
    def handle(self, **options):
        removed = clean_orphan_object_perms()
        if options['verbosity'] > 0:
            print('Removed %d object permission entries with no targets' % removed)
