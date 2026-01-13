from django.utils.deprecation import MiddlewareMixin


class LSCacheMiddleware(MiddlewareMixin):
def process_response(self, request, response):
cache_control = getattr(request, '_lscache_control', None)
if cache_control:
response['X-LiteSpeed-Cache-Control'] = cache_control
return response