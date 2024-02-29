import json
from django.http import JsonResponse


def get_request_data(request):
    try:
        # if request.method == 'POST':
        data = json.loads(request.body)
        return data
    except:
        return JsonResponse({"message": "Error retrieving request data", "code": "500"})
