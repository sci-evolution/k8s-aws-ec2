from datetime import datetime, timezone
from typing import Any, Dict, List
from .interfaces import (
    IModelCustomGetAll,
    IModelCustomGetByParams,
    IModelCustomGetById,
    IModelCustomCreate,
    IModelCustomUpdate,
    IModelCustomDelete,
    IServiceGetAll,
    IServiceGetByParams,
    IServiceGetById,
    IServiceCreate,
    IServiceUpdate,
    IServiceDelete
)


class TaskService(
    IServiceGetAll,
    IServiceGetByParams,
    IServiceGetById,
    IServiceCreate,
    IServiceUpdate,
    IServiceDelete
):
    """
    Service layer for Task business logic.

    Implements:
        - IServiceGetAll
        - IServiceGetByParams
        - IServiceGetById
        - IServiceCreate
        - IServiceUpdate
        - IServiceDelete
    """

    def __repr__(self) -> str:
        """
        Return a string representation of the TaskService instance.
        """
        return "<TaskService>"

    def get_all(self, model: IModelCustomGetAll) -> List[Dict[str, Any]]:
        """
        Retrieve all tasks from the model.
        """
        return model.custom_get_all()

    def get_by_params(self, model: IModelCustomGetByParams, param: str) -> List[Dict[str, Any]]:
        """
        Retrieve tasks from the model filtered by parameters.
        """
        return model.custom_get_by_params(param)

    def get_by_id(self, model: IModelCustomGetById, id: str) -> Dict[str, Any]:
        """
        Retrieve a single task by its ID from the model.
        """
        return model.custom_get_by_id(id)

    def create(self, model: IModelCustomCreate, data: Dict[str, Any]) -> bool:
        """
        Create a new task in the model.
        """
        return model.custom_create(data)

    def update(self, model: IModelCustomUpdate, data: Dict[str, Any]) -> bool:
        """
        Update a task in the model. If status is set to DONE, set end_time to now.
        """
        if data.get('status') == 'DONE':
            data['end_time'] = datetime.now(timezone.utc)
        return model.custom_update(data)

    def delete(self, model: IModelCustomDelete, id: str) -> bool:
        """
        Delete a task from the model by ID.
        """
        return model.custom_delete(id)
