import base64
from django.contrib.auth import authenticate
from django.http import HttpResponse

class BasicAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get('Authorization')

        if auth_header and auth_header.startswith('Basic '):
            credentials = base64.b64decode(auth_header.split(' ')[1]).decode('utf-8')
            username, password = credentials.split(':')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                request.user = user
            else:
                return HttpResponse('Unauthorized', status=401)

        response = self.get_response(request)
        return response
