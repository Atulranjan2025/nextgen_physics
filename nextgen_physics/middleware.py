from django.utils.deprecation import MiddlewareMixin
import os

class ForceSecureCookiesMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        mode = os.getenv("MODE", "local")
        if mode == "production":
            response["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
            response["X-Content-Type-Options"] = "nosniff"
            response["X-Frame-Options"] = "DENY"
        return response

print("✅ ForceSecureCookiesMiddleware loaded successfully (auto switch local/production)")
