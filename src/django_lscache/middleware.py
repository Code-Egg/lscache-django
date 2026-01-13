from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class LSCacheMiddleware(MiddlewareMixin):
    """
    LiteSpeed Cache Middleware for Django
    """

    def process_response(self, request, response):
        if request.method not in ("GET", "HEAD") or response.status_code != 200:
            return response

        skip_cookies = getattr(settings, "LSCACHE_SKIP_COOKIES", [])
        for cookie in skip_cookies:
            if cookie in request.COOKIES:
                response["X-LiteSpeed-Cache-Control"] = "private,no-cache"
                return response

        default_max_age = getattr(settings, "LSCACHE_DEFAULT_MAX_AGE", 60)
        default_cacheability = getattr(settings, "LSCACHE_DEFAULT_CACHEABILITY", "public")
        default_esi = getattr(settings, "LSCACHE_ESI_ENABLED", False)

        lscache_attr = getattr(request, "_lscache", None)
        if lscache_attr:
            header_value = []
            if "max_age" in lscache_attr:
                header_value.append(f"max-age={lscache_attr['max_age']}")
            if "cacheability" in lscache_attr:
                header_value.append(lscache_attr["cacheability"])
            if "esi" in lscache_attr and lscache_attr["esi"]:
                header_value.append("esi=on")
            response["X-LiteSpeed-Cache-Control"] = ",".join(header_value)
        else:
            header_value = [f"max-age={default_max_age}", default_cacheability]
            if default_esi:
                header_value.append("esi=on")
            response["X-LiteSpeed-Cache-Control"] = ",".join(header_value)

        return response