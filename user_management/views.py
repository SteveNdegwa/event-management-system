import ast
import json
from django.http import HttpResponse, JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt
import os
from dotenv import load_dotenv

from user_management.models import CachedUserRequest

# Load environment variables from .env file
load_dotenv()
USER_MANAGEMENT_API = os.getenv('USER_MANAGEMENT_API')


@csrf_exempt
def login(request):
    data = json.loads(request.body)
    url = f"{USER_MANAGEMENT_API}/login/"
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(response.json())
        CachedUserRequest.objects.create(request_type='login', request_data=data, response_data=response.json(), is_successful=True)
    else:
        CachedUserRequest.objects.create(request_type='login', request_data=data, response_data=response.json(), is_successful=False)
    return JsonResponse(response.json())


@csrf_exempt
def logout(request):
    data = json.loads(request.body)
    url = f"{USER_MANAGEMENT_API}/logout/"
    response = requests.get(url, json=data)
    if response.status_code == 200:
        print(response.json())
        CachedUserRequest.objects.create(request_type='logout', request_data={data}, response_data=response.json(), is_successful=True)
    else:
        CachedUserRequest.objects.create(request_type='logout', request_data={data}, response_data=response.json(), is_successful=False)
    return JsonResponse(response.json())


@csrf_exempt
def register(request):
    data = json.loads(request.body)
    url = f"{USER_MANAGEMENT_API}/register/"
    response = requests.post(url, json=data)
    if response.status_code == 201:
        CachedUserRequest.objects.create(request_type='register', request_data=data, response_data=response.json(), is_successful=True)
    else:
        CachedUserRequest.objects.create(request_type='register', request_data=data, response_data=response.json(), is_successful=False)
    return JsonResponse(response.json())


@csrf_exempt
def verify_user(request):

    url = f"{USER_MANAGEMENT_API}/"
    response = requests.post(url)
    return HttpResponse(response)