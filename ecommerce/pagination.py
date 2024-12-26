from rest_framework.pagination import LimitOffsetPagination

class MyCustomPagination(LimitOffsetPagination):
    """
    A limit/offset based style. For example:

    http://api.example.org/accounts/?limit=100
    http://api.example.org/accounts/?offset=400&limit=100
    """
    default_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = None
 