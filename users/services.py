from datetime import datetime
from django.db.models import Q
from .models import User
#######################################
from .interfaces import IServiceGetById
#######################################


class UserService(IServiceGetById):
    """
    It handles user's business rules
    """

    def _datetimetoiso(self, dt: datetime) -> str:
        return dt.replace(second=0, tzinfo=None,).isoformat()

    def _isotodatetime(self, iso: str) -> datetime:
        return datetime.fromisoformat(iso + "Z")

    def get_all(self) -> list[dict[str, any]]:
        return list(User.objects.all().values())
    
    def get_by_params(self, param: str) -> list[dict[str, any]]:
        return list(User.objects.filter(
            Q(name__icontains=param) |
            Q(gender__icontains=param) |
            Q(age__icontains=param)
        ).values())
    
    def get_by_id(self, user_id: str) -> dict[str, any]:
        user = User(user_id = user_id).get_by_id()
        userDict = {
            "user_id": user.user_id,
            "name": user.name,
            "gender_choices": user.gender_choices,
            "gender": user.gender,
            "age": user.age,
            "joined_at": user.joined_at,
            "is_active": user.is_active,
            "obs": user.obs
        }

        if(userDict["joined_at"]):
            userDict["joined_at"] = self._datetimetoiso(userDict["joined_at"])

        return userDict
    
    def create(self, user: dict[str, any]) -> bool:
        created = False
        joined = None
        
        if(user["joined_at"]):
            joined = self._isotodatetime(user["joined_at"])
        
        usr = User(
            name = user["name"],
            gender = user["gender"],
            age = user["age"],
            joined_at = joined,
            is_active = user["is_active"],
            obs = user["obs"]
        )

        if(usr.save()):
            created = True
        
        return created
    
    def update(self, user: dict[str, any]) -> bool:
        joined = None

        if(user["joined_at"]):
            joined = self._isotodatetime(user["joined_at"])
        
        usr = User(
            user_id = user["user_id"],
            name = user["name"],
            gender = user["gender"],
            age = user["age"],
            joined_at = joined,
            is_active = user["is_active"],
            obs = user["obs"]
        )

        return usr.custom_update()
    
    def delete(self, user_id: str) -> bool:
        usr = User(user_id = user_id)
        return usr.custom_delete()
