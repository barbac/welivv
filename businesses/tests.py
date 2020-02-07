import pytest
import json
from unittest.mock import MagicMock
from django.test import TestCase, RequestFactory
from django import test
from . import models, views


# These are poor man's fixtures
# To improve the test suit i would spend more time on this choosing more use
# cases and moving them to ither django's fixtures or pytest's.
PARAMETERS = dict(
    name="Yundt-Flatley",
    address="1386 Lim Brooks",
    address2="Suite 517",
    city="Lake Betsy",
    state="IA",
    zip="19416",
    country="US",
    phone="4034880719",
    website="http://www.halvorson.com/",
    created_at="2012-12-10 16:17:58+00:00",
)
SAVED_VALUES = PARAMETERS.copy()
SAVED_VALUES["uuid"] = "2859d6e0-1cb9-4fe9-bc00-97823a9fa4cb"

PARAMETERS2 = dict(
    name="Botsford Ltd",
    address="74883 Hane Prairie",
    address2="",
    city="Margrettburgh",
    state="KS",
    zip="99840",
    country="US",
    phone="2462288476",
    website="http://bergstrom.org/",
    created_at="2013-11-19 23:26:13+00:00",
)
# 'd083169c-4340-4a07-b390-07d297823efd'


def test_Business_get(db):
    business = models.Business(**SAVED_VALUES)
    business.save()

    mock_request = MagicMock()
    mock_request.GET.dict.return_value = {}
    response_businesses = views.Business().get(mock_request).content.decode("utf-8")
    response_businesses = json.loads(response_businesses)
    assert len(response_businesses) == 1  # a single record
    response_businesses[0].pop("id")
    assert SAVED_VALUES == response_businesses[0]


def test_Business_get_find_by_state(db):
    business = models.Business(**SAVED_VALUES)
    business.save()

    mock_request = MagicMock()
    mock_request.GET.dict.return_value = {"state": PARAMETERS["state"]}
    response_businesses = views.Business().get(mock_request).content.decode("utf-8")
    response_businesses = json.loads(response_businesses)
    assert len(response_businesses) == 1  # a single record
    response_businesses[0].pop("id")
    assert SAVED_VALUES == response_businesses[0]


def test_Business_get_find_by_address1(db):
    business = models.Business(**SAVED_VALUES)
    business.save()
    business2 = models.Business(**PARAMETERS2)
    business2.save()

    address = "lim brooks"  # all lower case incomplete address
    mock_request = MagicMock()
    mock_request.GET.dict.return_value = {"address": address}
    response_businesses = views.Business().get(mock_request).content.decode("utf-8")
    response_businesses = json.loads(response_businesses)
    assert len(response_businesses) == 1  # a single record
    response_businesses[0].pop("id")
    assert SAVED_VALUES == response_businesses[0]


def test_Business_get_find_by_address2(db):
    business = models.Business(**SAVED_VALUES)
    business.save()
    business2 = models.Business(**PARAMETERS2)
    business2.save()

    # 2nd addres
    address = "Suite 517"
    mock_request = MagicMock()
    mock_request.GET.dict.return_value = {"address": address}
    response_businesses = views.Business().get(mock_request).content.decode("utf-8")
    response_businesses = json.loads(response_businesses)
    assert len(response_businesses) == 1  # a single record
    response_businesses[0].pop("id")
    assert SAVED_VALUES == response_businesses[0]


def test_Business_get_find_by_non_exisiting_state(db):
    business = models.Business(**SAVED_VALUES)
    business.save()

    mock_request = MagicMock()
    mock_request.GET.dict.return_value = {"state": "WRONG STATE"}
    response_businesses = views.Business().get(mock_request).content.decode("utf-8")
    response_businesses = json.loads(response_businesses)
    assert len(response_businesses) == 0  # no records
