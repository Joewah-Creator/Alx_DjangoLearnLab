# LibraryProject/middleware.py
from django.conf import settings

class CSPMiddleware:
    """
    Minimal middleware to set a Content-Security-Policy header.
    The policy values are read from settings (CSP_*).
    """
    def __init__(self, get_response):
        self.get_response = get_response

        # build a basic policy string from settings
        default_src = " ".join(settings.CSP_DEFAULT_SRC) if getattr(settings, "CSP_DEFAULT_SRC", None) else "'self'"
        script_src = " ".join(getattr(settings, "CSP_SCRIPT_SRC", ("'self'",)))
        style_src = " ".join(getattr(settings, "CSP_STYLE_SRC", ("'self'",)))
        self.policy = f"default-src {default_src}; script-src {script_src}; style-src {style_src};"

    def __call__(self, request):
        response = self.get_response(request)
        # Only set header if not already set
        if 'Content-Security-Policy' not in response:
            response['Content-Security-Policy'] = self.policy
        return response
