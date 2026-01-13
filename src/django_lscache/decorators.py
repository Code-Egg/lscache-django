from functools import wraps

def lscache(max_age=None, cacheability=None, esi=False):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            request._lscache = {
                "max_age": max_age,
                "cacheability": cacheability,
                "esi": esi
            }
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
