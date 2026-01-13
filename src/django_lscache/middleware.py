# middleware.py
from django.conf import settings

class LSCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.skip_cookies = getattr(settings, "LSCACHE_SKIP_COOKIES", [])

    def __call__(self, request):
        if any(cookie in request.COOKIES for cookie in self.skip_cookies):
            request._lscache_private = False  # Treat as public
        else:
            request._lscache_private = True   # Default behavior

        response = self.get_response(request)

        if getattr(request, "_lscache_private", False):
            response["x-litespeed-cache"] = "hit,private"
        else:
            response["x-litespeed-cache"] = "hit"

        return response
