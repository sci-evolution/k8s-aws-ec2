from abc import ABC, abstractmethod
from django.http import HttpRequest, HttpResponse


class IViewGetById(ABC):
    @abstractmethod
    def get_by_id(self, HttpRequest, str, IServiceGetById) -> HttpResponse:
        pass

class IServiceGetById(ABC):
    @abstractmethod
    def get_by_id(self, str) -> dict[str, any]:
        pass

class IModelGetById(ABC):
    @abstractmethod
    def get_by_id(self):
        pass
