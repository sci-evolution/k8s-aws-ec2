import uuid
from datetime import datetime
from django.urls import reverse
from django.test import TestCase
from .models import User


DATA = {
    "user_id": None,
    "name": "User",
    "gender": "Male",
    "age": 50,
    "joined_at": datetime.now(),
    "is_active": True,
    "obs": "User for test"
}

class UserModelTest(TestCase):
    """
    Testing class for UserModel
    """

    def test_properties(self):
        """
        It should set all its properties correctly
        """

        user = User(
            user_id: DATA["user_id"],
            name: DATA["name"],
            gender: DATA["gender"],
            age: DATA["age"],
            joined_at: DATA["joined_at"],
            is_active: DATA["is_active"],
            obs: DATA["obs"]
        )

        self.assertEqual([
            user.user_id,
            user.name,
            user.gender,
            user.age,
            user.joined_at,
            user.is_active,
            user.obs
        ], [
            DATA["user_id"],
            DATA["name"],
            DATA["gender"],
            DATA["age"],
            DATA["joined_at"],
            DATA["is_active"],
            DATA["obs"]
        ])


class UserServiceTest(TestCase):
    """
    Testing class for UserService
    """

    def test_datetimetoiso(self):
        """
        It should receive an UTC datetime and return an ISO formatted string
        """
        pass

    def test_isotodatetime(self):
        """
        It should receive an ISO formatted string and return an UTC datetime
        """
        pass

    def test_get_all(self):
        """
        It should return a list containing all users
        """
        pass

    def test_get_by_params(self):
        """
        It should return a list containing all users that meet given parameters
        """
        pass

    def test_get_by_id(self):
        """
        It should return an user accordingly with the given user_id
        """
        pass

    def test_create(self):
        """
        It should return True if the user was created
        """
        pass

    def test_update(self):
        """
        It should return True if the user was updated
        """
        pass

    def test_delete(self):
        """
        It should return True if the user was deleted
        """
        pass


class UserViewTest(TestCase):
    """
    Testing class for UserView
    """

    @classmethod
    def setUpTestData(cls):
        for i in range(5):
            User.objects.create(
                name = f'{DATA["name"]}_{i}',
                gender = DATA["gender"],
                age = DATA["age"],
                joined_at = DATA["joined_at"],
                is_active = DATA["is_active"],
                obs = DATA["obs"]
            )
    
    def test_index(self):
        """
        It should return all users
        """

        resp = self.client.get(reverse("users:index",))
        self.assertEqual(resp.status_code, 200)
    
    def test_get_by_params(self):
        """
        It should return all users that meet given params
        """

        resp = self.client.get(path="/users/", query_params={"q": "User"})
        self.assertEqual(resp.status_code, 200)
    
    def test_get_by_id(self):
        """
        It should return an user accordingly with given primary key
        """

        user = User.objects.create(
            name = f'{DATA["name"]}',
            gender = DATA["gender"],
            age = DATA["age"],
            joined_at = DATA["joined_at"],
            is_active = DATA["is_active"],
            obs = DATA["obs"]
        )

        resp = self.client.get(reverse("users:retrieve", args=[user.user_id]))
        self.assertEqual(resp.status_code, 200)

    def test_create(self):
        """
        It should redirect to index after create a new user
        """

        resp = self.client.post(
            path=reverse("users:create",),
            data=DATA,
            content_type="application/json",
            follow=True
        )
        self.assertEqual(resp.status_code, 200)
    
    def test_update(self):
        """
        It should:
            On success: redirect to updated user.
            On error: return 404 or 500 status code.
        """

        user= User.objects.get(name="User_1")

        ok = {
            "user_id": user.user_id,
            "name": "Success",
            "gender": "Male",
            "age": 43,
            "joined_at": "",
            "is_active": False,
            "obs": "Correct date"
        }

        not_found = {
            "user_id": uuid.uuid4,
            "name": "Not Found",
            "gender": "Male",
            "age": 34,
            "joined_at": "",
            "is_active": False,
            "obs": "Incorrect user id"
        }

        db_error = {
            "user_id": user.user_id,
            "name": None,
            "gender": "Male",
            "age": 43,
            "joined_at": "",
            "is_active": False,
            "obs": "Incorrect data"
        }

        resp_200 = self.client.post(
            path=reverse("users:update", args=[ok["user_id"]]),
            data=ok,
            content_type="application/json",
            follow=True
        )
        resp_404 = self.client.post(
            path=reverse("users:update", args=[not_found["user_id"]]),
            data=not_found,
            content_type="application/json",
            follow=True
        )
        resp_500 = self.client.post(
            path=reverse("users:update", args=[db_error["user_id"]]),
            data=db_error,
            content_type="application/json",
            follow=True
        )

        print(resp_200.status_code)
        self.assertRedirects(resp_200, reverse("users:retrieve", args=[ok["user_id"]]))

        print(resp_404.status_code)
        self.assertEqual(resp_404.status_code, 404)

        print(resp_500.status_code)
        self.assertEqual(resp_500.status_code, 500)

    def test_delete(self):
        """
        It should redirect to index after delete an user
        """

        user = User.objects.get(name="User_1")
        resp = self.client.post(
            path=reverse("users:delete", args=[user.user_id]),
            follow=True
        )
        self.assertEqual(resp.status_code, 200)
    
###############################################################################
from .interfaces import IViewGetById, IServiceGetById


class TestUserView(TestCase):
    def test_get_by_id(self, IServiceGetById):
        """
        It should return an user accordingly with the given pk
        """
        pass

    def test_get_by_id(self, IServiceGetById):
        """
        It should return an user accordingly with given primary key 
        """
        pass
###############################################################################
