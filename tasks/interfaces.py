from abc import ABC, abstractmethod
from datetime import datetime
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect


###########################################################
###   Model Interfaces   ##################################
###########################################################
class IModelCustomGetAll(ABC):
    """ To get all items """

    @abstractmethod
    def custom_get_all(self) -> list[dict[str, any]]:
        pass

class IModelCustomGetByParams(ABC):
    """ To get items by given params """

    @abstractmethod
    def custom_get_by_params(self) -> list[dict[str, any]]:
        pass

class IModelCustomGetById(ABC):
    """ To get an item by its ID """

    @abstractmethod
    def custom_get_by_id(self) -> object:
        pass

class IModelCustomCreate(ABC):
    """ To create a new item """

    @abstractmethod
    def custom_create(self) -> bool:
        pass

class IModelCustomUpdate(ABC):
    """ To update an item """

    @abstractmethod
    def custom_update(self) -> bool:
        pass

class IModelCustomDelete(ABC):
    """ To delete an item """

    @abstractmethod
    def custom_delete(self) -> bool:
        pass


###########################################################
###   Service Interfaces   ################################
###########################################################
class IServiceGetAll(ABC):
    """ To get all items """

    @abstractmethod
    def get_all(self, model: IModelCustomGetAll) -> list[dict[str, any]]:
        pass

class IServiceGetByParams(ABC):
    """ To get items by given params """

    @abstractmethod
    def get_by_params(self, param: str, model: IModelCustomGetByParams) -> list[dict[str, any]]:
        pass

class IServiceGetById(ABC):
    """ To get an item by its id """
    @abstractmethod
    def get_by_id(self, id: str, model: IModelCustomGetById) -> dict[str, any]:
        pass

class IServiceCreate(ABC):
    """ To create a new item """

    @abstractmethod
    def create(self, model: IModelCustomCreate) -> bool:
        pass

class IServiceUpdate(ABC):
    """ To update an item """

    @abstractmethod
    def update(self, model: IModelCustomUpdate) -> bool:
        pass

class IServiceDelete(ABC):
    """ To delete an items """

    @abstractmethod
    def delete(self, model: IModelCustomDelete) -> bool:
        pass


###########################################################
###   View Interfaces   ###################################
###########################################################
class IViewGetAll(ABC):
    """ To get all items """

    @abstractmethod
    def get_all(self, request:HttpRequest, service: IServiceGetAll) -> HttpResponse:
        pass

class IViewGetByParams(ABC):
    """ To get items by given params """
    
    @abstractmethod
    def get_by_params(self, request:HttpRequest, service: IServiceGetByParams) -> HttpResponse:
        pass

class IViewGetById(ABC):
    """ To get an item by its id """
    
    @abstractmethod
    def get_by_id(self, request:HttpRequest, id: str, service: IServiceGetById) -> HttpResponse:
        pass

class IViewCreate(ABC):
    """ To create a new item """
    
    @abstractmethod
    def create(self, request:HttpRequest, service: IServiceCreate) -> HttpResponseRedirect:
        pass

class IViewUpdate(ABC):
    """ To update an item """
    
    @abstractmethod
    def update(self, request:HttpRequest, id: str, service: IServiceUpdate) -> HttpResponseRedirect:
        pass

class IViewDelete(ABC):
    """ To delete an items """
    
    @abstractmethod
    def delete(self, request:HttpRequest, id: str, service: IServiceDelete) -> HttpResponseRedirect:
        pass


###########################################################
###   Helper Interfaces   #################################
###########################################################
class IHelperDatetimeToIso(ABC):
    """ To convert a datetime into an ISO string """

    @abstractmethod
    def datetimetoiso(self, dt: datetime) -> str:
        pass

class IHelperIsoToDatetime(ABC):
    """ To convert an ISO string into a datetime """

    @abstractmethod
    def isotodatetime(self, iso: str) -> datetime:
        pass

class IHelperJSONDecode(ABC):
    """ To decode a json into a dict """

    @abstractmethod
    def json_decode(json: str) -> dict[str, any]:
        pass
