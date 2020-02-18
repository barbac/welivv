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


def json_response(data, status=200):
    return HttpResponse(serialize(data), content_type="application/json",
                        status=status
                        )


class BusinessForm(ModelForm):
    class Meta:
        model = models.Business
        fields = [
            "name",
            "address",
            "address2",
            "city",
            "state",
            "zip",
            "country",
            "phone",
            "website",
        ]


def error_message(message, status):
    return json_response(
        {"status": "error", "message": message,},
        status,
    )


def get_token_from_request(request):
    return request.headers.get('token', None)

def check_for_permission(profile, permission_codename):
    user = profile.user
    return user.has_perm(permission_codename)

@method_decorator(csrf_exempt, name="dispatch")
class Business(View):
    def get(self, request, *args, **kwargs):
        token = get_token_from_request(request)
        # print(request.HEADERS.get())
        if token is None:
            return error_message('No token found. you need to authenticate', 401)

        try:
            profile = models.UserProfile.objects.get(token=token)
        except models.UserProfile.DoesNotExist:
            #this means the token doens't exit in the db
            return error_message("unauthorized", 401)

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

    def put(self, request, *args, **kwargs):
        ###
        token = get_token_from_request(request)
        # print(request.HEADERS.get())
        if token is None:
            return error_message('No token found. you need to authenticate', 401)

        try:
            profile = models.UserProfile.objects.get(token=token)
        except models.UserProfile.DoesNotExist:
            #this means the token doens't exit in the db
            return error_message("unauthorized", 401)
        ###


        parameters = request.GET.dict()

        _id = parameters.pop("id", None)
        uuid = parameters.pop("uuid", None)
        if _id or uuid:
            if not check_for_permission(profile, 'welivv.update_business'):
                return error_message("forbidden", 403)

            # if we have an id or uuid it's an update

            ids = {}
            if _id:
                ids["id"] = _id
            if uuid:
                ids["uuid"] = uuid

            try:
                business = models.Business.objects.get(**ids)
                form = BusinessForm(parameters, instance=business)
                form.save()
            except models.Business.DoesNotExist:
                # they are giving an id or uuid but they don't match the same
                # record or don't exist.
                return json_response(
                    {"status": "error", "message": "ids don't match a business",}
                )
            except Exception:
                # As more methods and end points are define i'd create a base class
                # and reimplement dispatch for this kind of error catchers.
                return json_response({"status": "error",})
        else:
            # creating a new record.
            if not check_for_permission(profile, 'welivv.create_business'):
                return error_message("forbidden", 403)

            form = BusinessForm(parameters)
            if not form.is_valid():
                return json_response({"status": "error", "message": "Invalid data",})

            try:
                # record found. Don't create a new one.
                # Any difference in any field will create a new record.
                business = models.Business.objects.get(**form.cleaned_data)
            except models.Business.DoesNotExist:
                models.Business.objects.create(**parameters)
            except Exception:
                # As more methods and end points are define i'd create a base class
                # and reimplement dispatch for this kind of error catchers.
                return json_response({"status": "error"})

        return json_response({"status": "ok"})
