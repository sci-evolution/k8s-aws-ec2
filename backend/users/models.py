import uuid
from django.db import models, transaction


class User(models.Model):
    """
    It represents an User in the database
    """

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Name", max_length=50, null=False, blank=False)
    gender_choices = {"MALE": "Male", "FEMALE": "Female", "": ""}
    gender = models.CharField("Gender", max_length=6, choices=gender_choices, default="")
    age = models.IntegerField("Age", null=False, blank=False)
    joined_at = models.DateTimeField("Joined at", null=True, blank=True)
    is_active = models.BooleanField("Active", default=False, blank=True)
    obs = models.TextField("Observations", max_length=1000, default="", blank=True)

    def __str__(self) -> str:
        """
        returns a string representing an User object
        """
        
        user: dict[str, any] = {
            "user_id": self.user_id,
            "name": self.name,
            "gender_choices": self.gender_choices,
            "gender": self.gender,
            "age": self.age,
            "joined_at": self.joined_at,
            "is_active": self.is_active,
            "obs": self.obs
        }
        return str(user)
