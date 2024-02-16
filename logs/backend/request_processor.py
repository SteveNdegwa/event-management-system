import json


def get_request_data(request):
    data = {}
    if request.method == 'POST':
        data = json.loads(request.body)
    return data
