# url errors
class InvalidUrlPathError(Exception):
    "Error, URL path was sended with Endpoit or Null"
    pass

class InvalidUrlSchemeError(Exception):
    "Error, URL scheme was incorrect or None"
    pass

class InvalidUrlDomainError(Exception):
    "Error, URL have incorrect or None netloc"


# db general
class DatabaseError(Exception):
    "General database error exception"
    pass


# db special
class DatabaseDeleteError(Exception):
    "Error was raised on delete object"
    pass