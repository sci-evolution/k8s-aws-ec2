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

    def custom_get_by_id(self: Any, id: str) -> Dict[str, Any]:
        """
        Retrieves a single item by its id.
        Returns the item instance, or None if not found.
        """
        ...

class IModelCustomCreate(Protocol):
    """
    Protocol for models that support creating a new item.
    """

    def custom_create(self: Any, data: Dict[str, Any]) -> bool:
        """
        Creates a new item with the given data.
        Returns True if successful, False otherwise.
        """
        ...

class IModelCustomUpdate(Protocol):
    """
    Protocol for models that support updating an existing item.
    """

    def custom_update(self: Any, data: Dict[str, Any]) -> bool:
        """
        Updates the item with the given data.
        Returns True if successful, False otherwise.
        """
        ...

class IModelCustomDelete(Protocol):
    """
    Protocol for models that support deleting an item.
    """

    def custom_delete(self: Any, id: str) -> bool:
        """
        Deletes the item.
        Returns True if successful, False otherwise.
        """
        ...


###########################################################
###   Service Interfaces   ################################
###########################################################
class IServiceGetAll(ABC):
    """
    Interface for service to get all items from a model.
    """

    @abstractmethod
    def get_all(self: Any, model: IModelCustomGetAll) -> List[Dict[str, Any]]:
        """
        Retrieve all items from the model.
        """
        ...

class IServiceGetByParams(ABC):
    """
    Interface for service to get items by given params.
    """

    @abstractmethod
    def get_by_params(self: Any, model: IModelCustomGetByParams, param: str) -> List[Dict[str, Any]]:
        """
        Retrieve items by given params from the model.
        """
        ...

class IServiceGetById(ABC):
    """
    Interface for service to get an item by its id.
    """

    @abstractmethod
    def get_by_id(self: Any, model: IModelCustomGetById, id: str) -> Dict[str, Any]:
        """
        Retrieve an item by its id from the model.
        """
        ...

class IServiceCreate(ABC):
    """
    Interface for service to create a new item.
    """

    @abstractmethod
    def create(self: Any, model: IModelCustomCreate, data: Dict[str, Any]) -> bool:
        """
        Create a new item in the model.
        """
        ...

class IServiceUpdate(ABC):
    """
    Interface for service to update an item.
    """

    @abstractmethod
    def update(self: Any, model: IModelCustomUpdate, data: Dict[str, Any]) -> bool:
        """
        Update an item in the model.
        """
        ...

class IServiceDelete(ABC):
    """
    Interface for service to delete an item.
    """

    @abstractmethod
    def delete(self: Any, model: IModelCustomDelete, id: str) -> bool:
        """
        Delete an item from the model by id.
        """
        ...


###########################################################
###   View Interfaces   ###################################
###########################################################
class IViewGetAll(ABC):
    """
    Interface for view to get all items using a service.
    """

    @abstractmethod
    def get_all(self: Any, request: HttpRequest, service: IServiceGetAll) -> HttpResponse:
        """
        Get all items using the provided service.
        """
        ...

class IViewGetByParams(ABC):
    """
    Interface for view to get items by given params using a service.
    """

    @abstractmethod
    def get_by_params(self: Any, request: HttpRequest, service: IServiceGetByParams) -> HttpResponse:
        """
        Get items by given params using the provided service.
        """
        ...

class IViewGetById(ABC):
    """
    Interface for view to get an item by its id using a service.
    """

    @abstractmethod
    def get_by_id(self: Any, request: HttpRequest, id: str, service: IServiceGetById) -> HttpResponse:
        """
        Get an item by its id using the provided service.
        """
        ...

class IViewCreate(ABC):
    """
    Interface for view to create a new item using a service.
    """

    @abstractmethod
    def create(self: Any, request: HttpRequest, service: IServiceCreate) -> HttpResponseRedirect:
        """
        Create a new item using the provided service.
        """
        ...

class IViewUpdate(ABC):
    """
    Interface for view to update an item using a service.
    """

    @abstractmethod
    def update(self: Any, request: HttpRequest, service: IServiceUpdate) -> HttpResponseRedirect:
        """
        Update an item using the provided service.
        """
        ...

class IViewDelete(ABC):
    """
    Interface for view to delete an item using a service.
    """

    @abstractmethod
    def delete(self: Any, request: HttpRequest, service: IServiceDelete) -> HttpResponseRedirect:
        """
        Delete an item using the provided service.
        """
        ...


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
    """
    Interface for classes that can convert an ISO string into a datetime.
    """

    @abstractmethod
    def isotodatetime(self: Any, iso: str) -> datetime:
        """
        Convert an ISO string into a datetime object.
        """
        ...

class IHelperJSONDecode(ABC):
    """
    Interface for classes that can convert a JSON string into a dict.
    """

    @abstractmethod
    def json_decode(self: Any, json_src: str) -> Dict[str, Any]:
        """
        Convert a JSON string into a dictionary.
        """
        ...
