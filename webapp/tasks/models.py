import uuid
from typing import Any, List, Dict
from datetime import datetime
from django.db import models, transaction
from django.db.models import Q
from .exceptions import NotFound


class Task(models.Model):
    """
    Model class for User
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
        Meta class for Task model
        """

        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-start_time', 'priority', 'status']

    def __str__(self) -> str:
        """
        Returns a string representing an Task object
        """

        task: Dict[str, Any] = {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "PRIORITY_CHOICES": self.PRIORITY_CHOICES,
            "priority": self.priority,
            "STATUS_CHOICES": self.STATUS_CHOICES,
            "status": self.status
        }

        return str(task)
    
    def datetimetoiso(self, dt: datetime) -> str:
        """
        Converts a datetime object to an ISO 8601 formatted string.
        """

        iso: str = dt.replace(second=0, tzinfo=None,).isoformat()

        return iso

    def custom_get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all Tasks.
        """
    
        tasks: List[Dict[str, Any]] = list(self.__class__.objects.all().values())
    
        return tasks

    def custom_get_by_params(self, params: str) -> List[Dict[str, Any]]:
        """
        Retrieves items as a list of dictionaries, filtered by keyword arguments.
        """

        tasks: List[Dict[str, Any]] = list(self.__class__.objects.filter(
            Q(name__icontains=params) |
            Q(gender__icontains=params) |
            Q(age__icontains=params)
        ).values())

        return tasks

    def custom_get_by_id(self, id: str) -> Dict[str, Any]:
        """
        Retrieves a single Task by its primary key.
        """

        try:
            self: Task = Task.objects.get(pk=id)
            task: Dict[str, Any] = {
                "task_id": self.task_id,
                "title": self.title,
                "description": self.description,
                "start_time": self.datetimetoiso(self.start_time) if self.start_time else None,
                "end_time": self.datetimetoiso(self.end_time) if self.end_time else None,
                "PRIORITY_CHOICES": self.PRIORITY_CHOICES,
                "priority": self.priority,
                "STATUS_CHOICES": self.STATUS_CHOICES,
                "status": self.status
            }

            return task
        except Task.DoesNotExist as err:
            raise NotFound(err)

    def custom_create(self, data: Dict[str, Any]) -> bool:
        """
        Creates a new Task instance.
        """
        created = False

        try:
            with transaction.atomic():
                if not data["task_id"]:
                    self.title = data['title']
                    self.description = data['description']
                    self.start_time = data['start_time']
                    self.end_time = data['end_time']
                    self.priority = data['priority']
                    self.status = data['status']
                    self._state.adding = True
                    self.save()
                    created = True
        except Exception as err:
            raise Exception(f"Error creating Task: {err}")
        
        return created

    def custom_update(self, data: Dict[str, Any]) -> bool:
        """
        Updates a Task by using a transaction
        """

        updated = False

        try:
            with transaction.atomic():
                if(self.__class__.objects.get(pk=data['task_id'])):
                    self.task_id = data['task_id']
                    self.title = data['title']
                    self.description = data['description']
                    self.start_time = data['start_time']
                    self.end_time = data['end_time']
                    self.priority = data['priority']
                    self.status = data['status']
                    self._state.adding = False
                    self.save()
                    updated = True
        except Task.DoesNotExist as err:
            raise NotFound(err)

        return updated
    
    def custom_delete(self, id: str) -> bool:
        """
        Deletes a Task by using a transaction
        """

        deleted = False

        try:
            with transaction.atomic():
                if(self.__class__.objects.get(pk=id)):
                    self.task_id = id
                    self._state.adding = False
                    self.delete()
                    deleted = True
        except Task.DoesNotExist as err:
            raise NotFound(err)

        return deleted
