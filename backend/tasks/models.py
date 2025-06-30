import uuid
from typing import Any, List, Dict
from datetime import datetime
from django.db import models, transaction
from django.db.models import Q
from .exceptions import NotFound


class Task(models.Model):
    """
    Django model representing a Task entity.

    Implements:
        - IModelCustomGetAll
        - IModelCustomGetByParams
        - IModelCustomGetById
        - IModelCustomCreate
        - IModelCustomUpdate
        - IModelCustomDelete
    """
    task_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('task title', max_length=50)
    description = models.TextField('Task description', max_length=1000, default="", blank=True)
    start_time = models.DateTimeField('Start time', null=True, blank=True)
    end_time = models.DateTimeField('End time', null=True, blank=True)
    PRIORITY_CHOICES = { 'HIGH': 'High', 'MEDIUM': 'Medium', 'LOW': 'Low' }
    priority = models.CharField('Priority level', max_length=6, choices=PRIORITY_CHOICES, default='LOW')
    STATUS_CHOICES = { 'TODO': 'Todo', 'DOING': 'Doing', 'DONE': 'Done' }
    status = models.CharField('Task status', max_length=5, choices=STATUS_CHOICES, default='TODO')

    class Meta:
        """
        Meta class for Task model.
        """
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-start_time', 'priority', 'status']

    def __str__(self) -> str:
        """
        Returns a string representing a Task object for display purposes.
        """
        return f"Task(id={self.task_id}, title={self.title})"

    def __repr__(self) -> str:
        """
        Return a string representation of the Task instance for debugging.
        """
        task_dict: Dict[str, Any] = {
            "task_id": str(self.task_id),
            "title": self.title,
            "description": self.description,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "PRIORITY_CHOICES": self.PRIORITY_CHOICES,
            "priority": self.priority,
            "STATUS_CHOICES": self.STATUS_CHOICES,
            "status": self.status
        }
        return str(task_dict)

    def datetimetoiso(self, dt: datetime) -> str:
        """
        Converts a datetime object to an ISO 8601 formatted string.
        """
        iso: str = dt.replace(second=0, tzinfo=None,).isoformat()
        return iso

    def custom_get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all Tasks as a list of dictionaries.
        """
        tasks: List[Dict[str, Any]] = list(self.__class__.objects.all().values())
        return tasks

    def custom_get_by_params(self, params: str) -> List[Dict[str, Any]]:
        """
        Retrieves items as a list of dictionaries, filtered by keyword arguments.
        """
        tasks: List[Dict[str, Any]] = list(self.__class__.objects.filter(
            Q(title__icontains=params) |
            Q(priority__icontains=params) |
            Q(status__icontains=params)
        ).values())
        return tasks

    def custom_get_by_id(self, id: str) -> Dict[str, Any]:
        """
        Retrieves a single Task by its primary key.
        """
        try:
            retrieved_task: Task = Task.objects.get(pk=id)
            task: Dict[str, Any] = {
                "task_id": retrieved_task.task_id,
                "title": retrieved_task.title,
                "description": retrieved_task.description,
                "start_time": retrieved_task.datetimetoiso(retrieved_task.start_time) if retrieved_task.start_time else None,
                "end_time": retrieved_task.datetimetoiso(retrieved_task.end_time) if retrieved_task.end_time else None,
                "PRIORITY_CHOICES": retrieved_task.PRIORITY_CHOICES,
                "priority": retrieved_task.priority,
                "STATUS_CHOICES": retrieved_task.STATUS_CHOICES,
                "status": retrieved_task.status
            }
            return task
        except Task.DoesNotExist as err:
            raise NotFound(err)

    def custom_create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new Task instance from the provided data.
        """
        new_task: Task = None
        task: Dict[str, Any] = {}
        try:
            with transaction.atomic():
                new_task = Task.objects.create(
                    title=data['title'],
                    description=data['description'],
                    start_time=data['start_time'] if data.get('start_time') else None,
                    end_time=data['end_time'] if data.get('end_time') else None,
                    priority=data['priority'],
                    status=data['status']
                )
                task = {
                    "task_id": new_task.task_id,
                    "title": new_task.title,
                    "description": new_task.description,
                    "start_time": new_task.datetimetoiso(new_task.start_time) if new_task.start_time else None,
                    "end_time": new_task.datetimetoiso(new_task.end_time) if new_task.end_time else None,
                    "PRIORITY_CHOICES": new_task.PRIORITY_CHOICES,
                    "priority": new_task.priority,
                    "STATUS_CHOICES": new_task.STATUS_CHOICES,
                    "status": new_task.status
                }
        except Exception as err:
            raise Exception(f"Error creating Task: {err}")
        return task

    def custom_update(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates a Task instance with the provided data.
        """
        updated_task: Task = None
        task: Dict[str, Any] = {}
        try:
            with transaction.atomic():
                if updated_task.__class__.objects.get(pk=data['task_id']):
                    updated_task.title = data['title']
                    updated_task.description = data['description']
                    updated_task.start_time = data['start_time'] if data.get('start_time') else None
                    updated_task.end_time = data['end_time'] if data.get('end_time') else None
                    updated_task.priority = data['priority']
                    updated_task.status = data['status']
                    updated_task._state.adding = False
                    updated_task.save()
                task = {
                    "task_id": updated_task.task_id,
                    "title": updated_task.title,
                    "description": updated_task.description,
                    "start_time": updated_task.datetimetoiso(updated_task.start_time) if updated_task.start_time else None,
                    "end_time": updated_task.datetimetoiso(updated_task.end_time) if updated_task.end_time else None,
                    "PRIORITY_CHOICES": updated_task.PRIORITY_CHOICES,
                    "priority": updated_task.priority,
                    "STATUS_CHOICES": updated_task.STATUS_CHOICES,
                    "status": updated_task.status
                }
        except Task.DoesNotExist as err:
            raise NotFound(err)
        return task

    def custom_delete(self, id: str) -> bool:
        """
        Deletes a Task instance by its primary key.
        """
        deleted = False
        try:
            with transaction.atomic():
                if self.__class__.objects.get(pk=id):
                    self.task_id = id
                    self._state.adding = False
                    self.delete()
                    deleted = True
        except Task.DoesNotExist as err:
            raise NotFound(err)
        return deleted
