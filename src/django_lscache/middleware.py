class LSCacheMiddleware:
    """
    LiteSpeed Cache middleware for Django
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Before view (optional)
        response = self.get_response(request)
        # After view
        return self.process_response(request, response)

    def process_response(self, request, response):
        # Example: add LSCache headers
        from .conf import get_cache_control
        cache_header = get_cache_control(request)
        if cache_header:
            response["X-LiteSpeed-Cache-Control"] = cache_header
        return response
