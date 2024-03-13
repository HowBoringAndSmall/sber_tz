class ContentTypeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'CONTENT_TYPE' not in request.META:
            request.META['CONTENT_TYPE'] = 'application/json'
        return self.get_response(request)