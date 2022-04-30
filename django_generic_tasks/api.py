import inspect

from django.conf import settings
from ninja import NinjaAPI

from .security import BasicAuth
from .utils import import_attribute

auth = BasicAuth()
if path := getattr(settings, "TASKS_API_AUTHENTICATION", None):
    auth = import_attribute(path)
    if inspect.isclass(auth):
        auth = auth()
api = NinjaAPI(urls_namespace="tasks", auth=auth)
