class CustomSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        session_key = request.headers.get("x-session-key")
        if session_key:
            request.COOKIES["sessionid"] = session_key
        return self.get_response(request)
