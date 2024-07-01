class AllowIframeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if 'export_pdf' in request.path:
            response['X-Frame-Options'] = 'ALLOWALL'
        return response