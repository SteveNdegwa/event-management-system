import json
from django.http import JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt
from .backend.decorators import verify_token

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
USER_MANAGEMENT_API = os.getenv('USER_MANAGEMENT_API')


@csrf_exempt
def login(request):
    data = json.loads(request.body)
    url = f"{USER_MANAGEMENT_API}/login/"
    response = requests.post(url, json=data)
    return JsonResponse(response.json())


@csrf_exempt
def logout(request):
    data = json.loads(request.body)
    url = f"{USER_MANAGEMENT_API}/logout/"
    response = requests.post(url, json=data)
    return JsonResponse(response.json())


@csrf_exempt
def register(request):
    data = json.loads(request.body)
    url = f"{USER_MANAGEMENT_API}/register/"
    response = requests.post(url, json=data)
    return JsonResponse(response.json())


@csrf_exempt
def verify_user(request):
    url = f"{USER_MANAGEMENT_API}/"
    response = requests.post(url)
    return JsonResponse(response.json())