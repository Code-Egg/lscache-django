from functools import wraps


def lscache(max_age=60, public=True, esi=False):
def decorator(view_func):
@wraps(view_func)
def _wrapped_view(request, *args, **kwargs):
parts = [f"max-age={max_age}"]
parts.append('public' if public else 'private')
if esi:
parts.append('esi=on')
request._lscache_control = ';'.join(parts)
return view_func(request, *args, **kwargs)
return _wrapped_view
return decorator