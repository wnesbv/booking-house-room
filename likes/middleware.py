try:
    from hashlib import md5
except ImportError:
    from md5 import md5

from secretballot.middleware import SecretBallotIpUseragentMiddleware


class SecretBallotUserIpUseragentMiddleware(SecretBallotIpUseragentMiddleware):
    def generate_token(self, request):
        authenticated = request.user.is_authenticated
        if callable(authenticated):
            authenticated = authenticated()
        if authenticated:
            return request.user.username
        else:
            try:
                s = "".join((request.META["REMOTE_ADDR"], request.headers['User-Agent']))
                return md5(s.encode("utf-8")).hexdigest()
            except KeyError:
                return None
