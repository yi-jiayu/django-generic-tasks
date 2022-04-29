import abc
import inspect
from abc import abstractmethod
from typing import Generic, TypeVar, get_args

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from pydantic import BaseModel

from .api import router


def _fully_qualified_name(cls: type):
    return cls.__module__ + "." + cls.__qualname__


class TaskMeta(abc.ABCMeta):
    registry = {}

    def __new__(mcs, *args, **kwargs):
        cls = super().__new__(mcs, *args, **kwargs)
        if not inspect.isabstract(cls):
            name = _fully_qualified_name(cls)
            mcs.registry[name] = cls

            (params_type,) = get_args(cls.__orig_bases__[0])

            def handler(request, params: params_type):
                cls(params).run()
                return {}

            handler.__name__ = name

            # register HTTP handler
            router.post(
                f"/{name}", auth=getattr(settings, "TASKS_API_AUTHENTICATION", None)
            )(csrf_exempt(handler))

        return cls


Params = TypeVar("Params", bound=BaseModel)


class Task(Generic[Params], metaclass=TaskMeta):
    def __init__(self, params: Params):
        self.params = params

    @property
    def fully_qualified_name(self):
        return _fully_qualified_name(type(self))

    @abstractmethod
    def run(self):
        ...

    def start(self):
        backend = settings.TASKS_BACKEND
        backend.run(self)
