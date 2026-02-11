"""
Django Storage interface
"""
from django.utils.module_loading import import_string

from .. import appconfig

__all__ = (
    'private_storage',
    'PrivateStorage',
)

# Fetch the storage class
PrivateStorage = import_string(appconfig.PRIVATE_STORAGE_CLASS)

# Singleton instance.
private_storage = PrivateStorage()
