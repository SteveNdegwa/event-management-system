import json
from django.http import JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt

from services.request_processor import get_request_data
from .backend.ServiceLayer import CachedUserService

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
USER_MANAGEMENT_API = os.getenv('USER_MANAGEMENT_API')


@csrf_exempt
def login(request):
    data = get_request_data(request)
    url = f"{USER_MANAGEMENT_API}/login/"
    response = requests.post(url, json=data)
    user_data = response.json()['data']
    print(user_data)
    user_id = user_data.get('id')

    # check if cached data exists
    cached_data = CachedUserService().filter(user_id=user_id)
    if cached_data.exists():
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
            # role=user_data.get('role'),
            role="default",
        )

    # create cache data
    else:
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
            # role=user_data.get('role'),
            role="default",
        )

    return JsonResponse(response.json())


@csrf_exempt
def logout(request):
    data = get_request_data(request)
    url = f"{USER_MANAGEMENT_API}/logout/"
    response = requests.post(url, json=data)
    return JsonResponse(response.json())


@csrf_exempt
def register(request):
    data = get_request_data(request)
    url = f"{USER_MANAGEMENT_API}/register/"
    response = requests.post(url, json=data)
    return JsonResponse(response.json())

