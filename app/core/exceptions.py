# url errors
class InvalidUrlPathError(Exception):
    "Error, URL path was sended with Endpoit or Null"
    pass

class InvalidUrlSchemeError(Exception):
    "Error, URL scheme was incorrect or None"
    pass

class InvalidUrlDomainError(Exception):
    "Error, URL have incorrect or None netloc"
    pass


# endpoint errors
class EndpointIdError(Exception):
    "Error, Endpoint with this id dont exist"


# db general
class DatabaseError(Exception):
    "General database error exception"
    pass


# db special
class DatabaseDeleteError(Exception):
    "Error was raised on delete object"
    pass

class DatabaseGetError(Exception):
    "Error was raised during get object"
    pass