from django.http import JsonResponse
from functools import wraps
import requests
import os
from dotenv import load_dotenv

load_dotenv()
USER_MANAGEMENT_API = os.getenv('USER_MANAGEMENT_API')


def verify_token(inner_function):
    @wraps(inner_function)
    def _wrapped_function(request, *args, **kwargs):
        print("verifying token")
        token = request.COOKIES.get('token')
        print(token)
        url = f"{USER_MANAGEMENT_API}/"
        response = requests.post(url, json={"token": token})
        print(response)
        if response.json().data.code == "200":
            return inner_function(request, *args, **kwargs)
        return JsonResponse({"message": "Invalid Token"}, status=403)
    return _wrapped_function

