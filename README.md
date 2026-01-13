# django-lscache

This is a sample LiteSpeed Cache plugin for Django applications.

## Installation
```
pip install django-lscache
```

Add django_lscache module to settings.py
```
INSTALLED_APPS = [
    ...
    "django_lscache",
]
```
```
MIDDLEWARE = [
    ...
    "django_lscache.middleware.LSCacheMiddleware",
]
```

## Usage
Examples of using decorator in views:
```
from django_lscache.decorators import lscache
from django.http import HttpResponse

@lscache()
def index(request):
    return HttpResponse("Hello, world!")

@lscache(max_age=300)
def index(request):
    return HttpResponse("Hello, world!")   

@lscache(max_age=10, cacheability="private")
def contact(request):
    return HttpResponse("Contact page")
```
