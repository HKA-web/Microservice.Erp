import importlib.metadata

from .choices import Choices
from .tracker import FieldTracker, ModelTracker

try:
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = None

__all__ = [
    Choices,
    FieldTracker,
    ModelTracker,
]
