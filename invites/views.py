from invites.backend.request_processor import get_request_data


def invite_to_event(request):
    data = get_request_data(request)
