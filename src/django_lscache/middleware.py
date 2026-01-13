from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class LSCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.method not in ["GET", "HEAD"]:
            return response

        if any(cookie in request.COOKIES for cookie in getattr(settings, "LSCACHE_SKIP_COOKIES", [])):
            response["X-LiteSpeed-Cache-Control"] = "no-cache"
        elif "X-LiteSpeed-Cache-Control" not in response:
            max_age = getattr(settings, "LSCACHE_DEFAULT_MAX_AGE", 60)
            cacheability = getattr(settings, "LSCACHE_DEFAULT_CACHEABILITY", "public")
            response["X-LiteSpeed-Cache-Control"] = f"max-age={max_age},{cacheability}"

        return response
