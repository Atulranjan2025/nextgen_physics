# nextgen_physics/middleware.py

class ForceSecureCookiesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Apply only on HTTPS requests
        if request.is_secure():
            # ✅ Safely handle session cookie
            if 'sessionid' in response.cookies:
                response.cookies['sessionid']['secure'] = True
                response.cookies['sessionid']['samesite'] = 'None'

            # ✅ Safely handle CSRF cookie
            if 'csrftoken' in response.cookies:
                response.cookies['csrftoken']['secure'] = True
                response.cookies['csrftoken']['samesite'] = 'None'

        return response
