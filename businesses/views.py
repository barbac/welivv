import json
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.forms import ModelForm
from django.views.generic import View
from django.http import HttpResponse

from . import models


def serialize(data):
    return json.dumps(data, ensure_ascii=False, indent=2, default=lambda o: str(o))


def json_response(data):
    return HttpResponse(serialize(data), content_type="application/json")


@method_decorator(csrf_exempt, name="dispatch")
class Business(View):
    def get(self, request, *args, **kwargs):
        parameters = request.GET.dict()
        filter_kwargs = {}

        # There's only 3 so i didn't create a new function to avoid repetition.
        name = parameters.pop("name", None)
        if name:
            filter_kwargs["name__icontains"] = name

        city = parameters.pop("city", None)
        if city:
            filter_kwargs["city__icontains"] = city

        state = parameters.pop("state", None)
        if state:
            filter_kwargs["state__icontains"] = state

        address_value = parameters.pop("address", None)
        address = []
        if address_value:
            address = [
                Q(address__icontains=address_value)
                | Q(address2__icontains=address_value)
            ]

        businesses = list(
            models.Business.objects.filter(*address, **filter_kwargs).values()
        )
        return json_response(businesses)

