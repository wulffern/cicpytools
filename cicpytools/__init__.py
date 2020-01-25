from .version import __version__
from .tf2tech import tf2tech

# if somebody does "from somepackage import *", this is what they will
# be able to access:
__all__ = [
    'tf2tech',
]
