import uuid
from datetime import datetime
from django.urls import reverse
from django.test import TestCase

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
    IServiceDelete,
    IViewGetAll,
    IViewGetByParams,
    IViewGetById,
    IViewCreate,
    IViewUpdate,
    IViewDelete,
    IHelperDatetimeToIso,
    IHelperIsoToDatetime,
    IHelperJSONDecode
)


class TestTaskModel(TestCase):
    """ Testing class for TaskModel """

    def test_custom_get_all(self, model: IModelCustomGetAll):
        pass

    def test_custom_get_by_params(self, model: IModelCustomGetByParams):
        pass

    def test_custom_get_by_id(self, model: IModelCustomGetById):
        pass

    def test_custom_create(self, model: IModelCustomCreate):
        pass

    def test_custom_update(self, model: IModelCustomUpdate):
        pass

    def test_custom_delete(self, model: IModelCustomDelete):
        pass

class TestTaskService(TestCase):
    """ Testing class for TaskService """

    def test_get_all(self, service: IServiceGetAll):
        pass

    def test_get_by_params(self, service: IServiceGetByParams):
        pass

    def test_get_by_id(self, service: IServiceGetById):
        pass

    def test_create(self, service: IServiceCreate):
        pass

    def test_update(self, service: IServiceUpdate):
        pass

    def test_delete(self, service: IServiceDelete):
        pass

class TestTaskView(TestCase):
    """ Testing class for TaskView """

    def test_get_all(self, view: IViewGetAll):
        pass

    def test_get_by_params(self, view: IViewGetByParams):
        pass

    def test_get_by_id(self, view: IViewGetById):
        pass

    def test_create(self, view: IViewCreate):
        pass

    def test_update(self, view: IViewUpdate):
        pass

    def test_delete(self, view: IViewDelete):
        pass

class TestHelpers(TestCase):
    """ Testing class for helper functions """

    def test_datetimetoiso(self, helper: IHelperDatetimeToIso):
        pass

    def test_isotodatetime(self, helper: IHelperIsoToDatetime):
        pass

    def test_json_decode(self, helper: IHelperJSONDecode):
        pass
