from django.apps import AppConfig

class DjangoLSCacheConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_lscache"
    verbose_name = "LiteSpeed Cache"

def ready(self):
    from .conf import ensure_middleware
    ensure_middleware()
