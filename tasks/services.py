from datetime import datetime
from django.db.models import Q
from .models import Task
######################################################
from .interfaces import IServiceGetById, IModelCustomGetById
######################################################


class TaskService(IServiceGetById):
    """
    It handles task's business rules
    """

    def _datetimetoiso(self, dt: datetime) -> str:
        iso: str = dt.replace(second=0, tzinfo=None,).isoformat()
        return iso

    def _isotodatetime(self, iso: str) -> datetime:
        dt: datetime = datetime.fromisoformat(iso + "Z")
        return dt

    def get_all(self) -> list[dict[str, any]]:
        tasks: list[dict[str, any]] = list(Task.objects.all().values())
        return tasks
    
    def get_by_params(self, param: str) -> list[dict[str, any]]:
        tasks: list[dict[str, any]] = list(Task.objects.filter(
            Q(name__icontains=param) |
            Q(gender__icontains=param) |
            Q(age__icontains=param)
        ).values())
        return tasks
    
    def get_by_id(self, task_id: str, task: IModelCustomGetById) -> dict[str, any]:
        tsk = task(task_id = task_id).get_by_id()
        taskDict: dict[str: any] = {
            "task_id": tsk.task_id,
            "title": tsk.title,
            "description": tsk.description,
            "start_time": tsk.start_time,
            "end_time": tsk.end_time,
            "PRIORITY_CHOICES": tsk.PRIORITY_CHOICES,
            "priority": tsk.priority,
            "STATUS_CHOICES": tsk.STATUS_CHOICES,
            "status": tsk.status
        }

        if(taskDict["start_time"]):
            taskDict["start_time"] = self._datetimetoiso(taskDict["start_time"])
        
        if(taskDict["end_time"]):
            taskDict["end_time"] = self._datetimetoiso(taskDict["end_time"])

        return taskDict
    
    def create(self, task: dict[str, any]) -> bool:
        created = False
        start_time = None
        end_time = None

        if(task['start_time']):
            start_time = self._isotodatetime(task['start_time'])

        if(task['end_time']):
            end_time = self._isotodatetime(task['end_time'])

        tsk = Task(
            title=task['title'],
            description=task['description'],
            start_time=start_time,
            end_time=end_time,
            priority=task['priority'],
            status=task['status']
        )

        if(tsk.save()):
            created = True

        return created

    def update(self, task: dict[str, any]) -> bool:
        updated = False
        start_time = None
        end_time = None

        if(task['start_time']):
            start_time = self._isotodatetime(task['start_time'])

        if(task['end_time']):
            end_time = self._isotodatetime(task['end_time'])

        tsk = Task(
            task_id = task["task_id"],
            title=task['title'],
            description=task['description'],
            start_time=start_time,
            end_time=end_time,
            priority=task['priority'],
            status=task['status']
        )

        if(tsk.custom_update()):
            updated = True

        return updated
    
    def delete(self, task_id: str) -> bool:
        deleted = False
        tsk = Task(task_id = task_id)

        if(tsk.custom_delete()):
            deleted = True

        return deleted
