from django.http import Http404
from django.utils.deprecation import MiddlewareMixin
from .settings import DEBUG


class FilterIPMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if not DEBUG:
            not_allowed_ips = []
            ip = request.META.get('REMOTE_ADDR')
            if ip in not_allowed_ips:
                raise Http404
            return None


class ProfileMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.path.startswith('/admin/') or request.path.startswith('/account/') \
                or request.path.startswith('/logout/'):
            return None
