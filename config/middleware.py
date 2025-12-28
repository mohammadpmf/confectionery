from django.utils.translation import activate
from django.utils.deprecation import MiddlewareMixin


class AdminEnglishMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith("/admin/"):
            activate("en")
            request.LANGUAGE_CODE = "en"
        else:
            activate("fa")
            request.LANGUAGE_CODE = "fa"
