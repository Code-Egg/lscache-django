from django.conf import settings

def ensure_middleware():
    mw = "django_lscache.middleware.LSCacheMiddleware"
    if mw not in settings.MIDDLEWARE:
        settings.MIDDLEWARE.append(mw)
