from django.middleware.csrf import CsrfViewMiddleware
from django.utils.deprecation import MiddlewareMixin

class DisableCSRFForAPIMiddleware(MiddlewareMixin):
    """Disable CSRF check for /api/ endpoints - Token Auth is used instead"""
    
    def process_request(self, request):
        if request.path.startswith('/api/'):
            request.csrf_processing_done = True
        return None
