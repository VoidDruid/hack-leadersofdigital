# pylint: disable=C0413

from services.api import Api

api: Api = Api()

# Import routes here
# from .module import path  # isort:skip
from .parameter import *
from .program import *
