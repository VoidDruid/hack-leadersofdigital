# pylint: disable=C0413

from services.api import Api

api: Api = Api()

from .parameter import *  # isort:skip
from .program import *  # isort:skip
from .discipline import *  # isort:skip
