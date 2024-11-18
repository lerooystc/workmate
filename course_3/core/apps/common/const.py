class HttpMethod:
    GET: str = "get"
    POST: str = "post"
    PUT: str = "put"
    PATCH: str = "patch"
    DELETE: str = "delete"


class DjangoActions:
    LIST: str = "list"
    RETRIEVE: str = "retrieve"
    CREATE: str = "create"
    UPDATE: str = "update"
    PARTIAL_UPDATE: str = "partial_update"
    DESTROY: str = "destroy"
