from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication

class CsrfExemptTokenAuthentication(TokenAuthentication):
    def enforce_csrf(self, request):
        return  