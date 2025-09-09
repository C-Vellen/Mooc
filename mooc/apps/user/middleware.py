from datetime import datetime, timedelta
from django.contrib.auth import logout

from user.OpenID import OpenId
from mooc.settings import DEBUG

try:
    from .display_session import show_sessions, show_request
except ModuleNotFoundError:
    pass


class UserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """récupération des identifiants de l'utilisateur"""

        response = self.get_response(request)
        if request.session.get("user") == None:
            logout(request)
            print("============= NEW SESSION GUEST ===============")
            # Définir l'utilisateur invité :
            userinfo = {
                "subid": None,
                "username": None,
                "first_name": None,
                "last_name": None,
                "group": ["guest"],
                "restriction": None,
            }
            request.session["user"] = userinfo
            # utilisateur anonyme : session expire après 1h :
            request.session.set_expiry(3600)

        # show_sessions()
        # show_request(request)
        return response
