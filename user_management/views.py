import json
from django.http import JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt

from base.backend.ServiceLayer import StateService
from services.decorators import verify_token
from services.request_processor import get_request_data
from .backend.ServiceLayer import CachedUserService

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
USER_MANAGEMENT_API = os.getenv('USER_MANAGEMENT_API')


@csrf_exempt
@verify_token
def login(request):
    data = get_request_data(request)
    url = f"{USER_MANAGEMENT_API}/login/"
    response = requests.post(url, json=data)

    if response.status_code != 200:
        return JsonResponse(response.json())

    user_data = response.json()['data']
    user_id = user_data.get('uuid')

    # check if cached data exists
    cached_data = CachedUserService().filter(user_id=user_id).first()
    if cached_data:
        # update cached data
        CachedUserService().update(
            cached_data.uuid,
            username=user_data.get('username'),
            email=user_data.get('email'),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            is_superuser=user_data.get('is_superuser'),
            is_active=user_data.get('is_active'),
            is_staff=user_data.get('is_staff'),
            date_joined=user_data.get('date_joined'),
            last_login=user_data.get('last_login'),
            role=user_data.get('role'),
        )

    # create cache data
    else:
        state = StateService().get(name="active")
        CachedUserService().create(
            user_id=user_id,
            username=user_data.get('username'),
            email=user_data.get('email'),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            is_superuser=user_data.get('is_superuser'),
            is_active=user_data.get('is_active'),
            is_staff=user_data.get('is_staff'),
            date_joined=user_data.get('date_joined'),
            last_login=user_data.get('last_login'),
            role=user_data.get('role'),
            cached_user_state=state,
        )

    json_response = JsonResponse(response.json())
    # json_response.set_cookie('token', user_data.get('token'), httponly=True)
    json_response.set_cookie('user_id', user_data.get('uuid'), httponly=True)
    json_response.set_cookie('role', user_data.get('role'), httponly=True)

    return json_response


@csrf_exempt
def logout(request):
    json_response = JsonResponse({"message": "logout successful"}, status=200)
    json_response.delete_cookie('token')
    return json_response


@csrf_exempt
def register(request):
    data = get_request_data(request)
    url = f"{USER_MANAGEMENT_API}/register/"
    response = requests.post(url, json=data)
    return JsonResponse(response.json())


@csrf_exempt
def confirm_email(request):
    data = get_request_data(request)
    url = f"{USER_MANAGEMENT_API}/confirmEmail/"
    response = requests.post(url, json=data)
    return JsonResponse(response.json())


@csrf_exempt
def forgot_password(request):
    data = get_request_data(request)
    url = f"{USER_MANAGEMENT_API}/forgot/"
    response = requests.post(url, json=data)
    return JsonResponse(response.json())


@csrf_exempt
def reset_password(request):
    data = get_request_data(request)
    url = f"{USER_MANAGEMENT_API}/reset/"
    response = requests.post(url, json=data)
    return JsonResponse(response.json())


@csrf_exempt
def change_credentials(request):
    data = get_request_data(request)
    url = f"{USER_MANAGEMENT_API}/changecredentials/"
    response = requests.post(url, json=data)
    return JsonResponse(response.json())

