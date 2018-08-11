# encoding:utf-8

class UnauthorizedError(Exception):
    pass

class BadRequestError(Exception):
    pass

class NotFoundError(Exception):
    pass

class RestfulException(Exception):
    pass

