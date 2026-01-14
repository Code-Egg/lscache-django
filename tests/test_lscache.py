from django.test import RequestFactory, TestCase
from django.http import HttpResponse
from django_lscache.decorators import lscache
from django_lscache.middleware import LSCacheMiddleware


class LSCacheMiddlewareTest(TestCase):
def setUp(self):
self.factory = RequestFactory()
self.middleware = LSCacheMiddleware()


def test_cache_header_set(self):
@lscache(max_age=120)
def view(request):
return HttpResponse('Hello World')


request = self.factory.get('/')
response = view(request)
response = self.middleware.process_response(request, response)
self.assertEqual(response['X-LiteSpeed-Cache-Control'], 'max-age=120;public')