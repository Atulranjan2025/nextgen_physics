# Force secure cookies for Render (fix admin login)
class ForceSecureCookiesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.is_secure():
            # Force session and CSRF cookies to be marked secure
            response.cookies['sessionid']['secure'] = True
            response.cookies['sessionid']['samesite'] = 'None'
            if 'csrftoken' in response.cookies:
                response.cookies['csrftoken']['secure'] = True
                response.cookies['csrftoken']['samesite'] = 'None'
        return response
