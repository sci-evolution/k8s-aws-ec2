from abc import ABC, abstractmethod
from datetime import datetime
from typing import Protocol, List, Dict, Any
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect


###########################################################
###   Model Interfaces   ##################################
###########################################################

# --- Interfaces defined using typing.Protocol ---

class IModelCustomGetAll(Protocol):
    """
    Protocol for models that support retrieving all items.
    """
    def custom_get_all(self: Any) -> List[Dict[str, Any]]:
        """
        Retrieves all items as a list of dictionaries.
        """
        ...

class IModelCustomGetByParams(Protocol):
    """
    Protocol for models that support retrieving items by given parameters.
    """
    def custom_get_by_params(self: Any, params: str) -> List[Dict[str, Any]]:
        """
        Retrieves items as a list of dictionaries, filtered by keyword arguments.
        """
        ...

class IModelCustomGetById(Protocol):
    """
    Protocol for models that support retrieving a single item by its ID.
    """
    def custom_get_by_id(self: Any, id: Any) -> Dict[str, Any]:
        """
        Retrieves a single item by its id.
        Returns the item instance, or None if not found.
        """
        ...

class IModelCustomCreate(Protocol):
    """
    Protocol for models that support creating a new item.
    """
    def custom_create(self: Any) -> bool:
        """
        Creates a new item with the given data.
        Returns True if successful, False otherwise.
        """
        ...

class IModelCustomUpdate(Protocol):
    """
    Protocol for models that support updating an existing item.
    """
    def custom_update(self: Any) -> bool:
        """
        Updates the item with the given data.
        Returns True if successful, False otherwise.
        """
        ...

class IModelCustomDelete(Protocol):
    """
    Protocol for models that support deleting an item.
    """
    def custom_delete(self: Any) -> bool:
        """
        Deletes the item.
        Returns True if successful, False otherwise.
        """
        ...


###########################################################
###   Service Interfaces   ################################
###########################################################
class IServiceGetAll(ABC):
    """ To get all items """

    @abstractmethod
    def get_all(self: Any, model: IModelCustomGetAll) -> List[Dict[str, Any]]:
        pass

class IServiceGetByParams(ABC):
    """ To get items by given params """

    @abstractmethod
    def get_by_params(self: Any, param: str, model: IModelCustomGetByParams) -> List[Dict[str, Any]]:
        pass

class IServiceGetById(ABC):
    """ To get an item by its id """
    @abstractmethod
    def get_by_id(self: Any, id: str, model: IModelCustomGetById) -> Dict[str, Any]:
        pass

class IServiceCreate(ABC):
    """ To create a new item """

    @abstractmethod
    def create(self: Any, model: IModelCustomCreate) -> bool:
        pass

class IServiceUpdate(ABC):
    """ To update an item """

    @abstractmethod
    def update(self: Any, model: IModelCustomUpdate) -> bool:
        pass

class IServiceDelete(ABC):
    """ To delete an items """

    @abstractmethod
    def delete(self: Any, model: IModelCustomDelete) -> bool:
        pass


###########################################################
###   View Interfaces   ###################################
###########################################################
class IViewGetAll(ABC):
    """ To get all items """

    @abstractmethod
    def get_all(self: Any, request:HttpRequest, service: IServiceGetAll) -> HttpResponse:
        pass

class IViewGetByParams(ABC):
    """ To get items by given params """
    
    @abstractmethod
    def get_by_params(self: Any, request:HttpRequest, service: IServiceGetByParams) -> HttpResponse:
        pass

class IViewGetById(ABC):
    """ To get an item by its id """
    
    @abstractmethod
    def get_by_id(self: Any, request:HttpRequest, id: str, service: IServiceGetById) -> HttpResponse:
        pass

class IViewCreate(ABC):
    """ To create a new item """
    
    @abstractmethod
    def create(self: Any, request:HttpRequest, service: IServiceCreate) -> HttpResponseRedirect:
        pass

class IViewUpdate(ABC):
    """ To update an item """
    
    @abstractmethod
    def update(self: Any, request:HttpRequest, id: str, service: IServiceUpdate) -> HttpResponseRedirect:
        pass

class IViewDelete(ABC):
    """ To delete an items """
    
    @abstractmethod
    def delete(self: Any, request:HttpRequest, id: str, service: IServiceDelete) -> HttpResponseRedirect:
        pass


###########################################################
###   Helper Interfaces   #################################
###########################################################
class IHelperDatetimeToIso(Protocol):
    """
    Protocol for classes that can convert a datetime object to an ISO 8601 string.
    """
    def datetimetoiso(self: Any, dt: datetime) -> str:
        """
        Converts a datetime object to an ISO 8601 formatted string.
        """
        ...

class IHelperIsoToDatetime(ABC):
    """ To convert an ISO string into a datetime """

    @abstractmethod
    def isotodatetime(self: Any, iso: str) -> datetime:
        pass

class IHelperJSONDecode(ABC):
    """ To convert a json into a dict """

    @abstractmethod
    def json_decode(self: Any, json_src: str) -> Dict[str, Any]:
        pass
