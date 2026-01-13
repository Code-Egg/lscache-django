from functools import wraps
from django.conf import settings

def lscache(max_age=None, cacheability=None):
    if max_age is None:
        max_age = getattr(settings, "LSCACHE_DEFAULT_MAX_AGE", 60)
    if cacheability is None:
        cacheability = getattr(settings, "LSCACHE_DEFAULT_CACHEABILITY", "public")

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)

            if any(cookie in request.COOKIES for cookie in getattr(settings, "LSCACHE_SKIP_COOKIES", [])):
                response["X-LiteSpeed-Cache-Control"] = "no-cache"
            else:
                response["X-LiteSpeed-Cache-Control"] = f"max-age={max_age},{cacheability}"

            return response
        return wrapper

    return decorator
