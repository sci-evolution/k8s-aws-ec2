import uuid
from django.db import models, transaction
from tasks.exceptions import NotFound
from interfaces import IModelCustomGetById, IModelCustomUpdate, IModelCustomDelete


class Task(models.Model, IModelCustomGetById, IModelCustomUpdate, IModelCustomDelete):
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

    def __str__(self) -> str:
        """
        Returns a string representing an Task object
        """

        task = dict[str, any] ={
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
    
    def get_by_id(self) -> object:
        """
        Get an Task by its id
        """

        try:
            self = Task.objects.get(pk=self.task_id)

            return self
        except Task.DoesNotExist as err:
            raise NotFound(err)
    
    def custom_update(self) -> bool:
        """
        Updates a Task by using a transaction
        """

        updated = False

        try:
            with transaction.atomic():
                if(Task.objects.get(pk=self.task_id)):
                    self._state.adding = False
                    self.save()
                    updated = True
        except Task.DoesNotExist as err:
            raise NotFound(err)

        return updated
    
    def custom_delete(self) -> bool:
        """
        Deletes a by using a transaction
        """

        deleted = False

        try:
            with transaction.atomic():
                if(Task.objects.get(pk=self.task_id)):
                    self._state.adding = False
                    self.delete()
                    deleted = True
        except Task.DoesNotExist as err:
            raise NotFound(err)

        return deleted
