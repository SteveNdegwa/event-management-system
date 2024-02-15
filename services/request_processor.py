import json
from django.http import JsonResponse


def get_request_data(request):
    try:
        # if request.method == 'POST':
        data = json.loads(request.body)
        user_id = request.COOKIES.get('user_id')
        token = request.COOKIES.get('token')
        if user_id:
            data.user_id = user_id
        if token:
            data.token = token
        return data
    except:
        return JsonResponse({"message": "Error retrieving request data", "code": "500"}, status=500)
