"""
List the settings defined via the YAMLCONF module.
"""
from yamlconfig import list_attrs
from yamlconfig.management.commands import YCBaseCommand


class Command(YCBaseCommand):
    """
    Implementation class for the "yclist" Django management command.
    """

    def handle(self, *args, **options):
        """
        Handle, i.e., execute, the command given the command line arguments
        "args" and "options".
        """
        super(Command, self).handle(*args, **options)
        list_attrs(stream=self.stdout)
