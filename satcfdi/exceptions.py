class CFDIError(Exception):
    """
    CFDI Error
    """


class SchemaValidationError(Exception):
    """
    Schema Validation Error
    """

    def __init__(self, error_log):
        self.error_log = error_log
        super().__init__(error_log)


class ResponseError(Exception):
    """
    Request Response Error
    """

    def __init__(self, response):
        self.response = response
        super().__init__(response)


class NamespaceMismatchError(Exception):
    """
    Returned by objectify and xmlify
    """

    def __init__(self, node):
        self.node = node
        super().__init__(node)


class DocumentNotFoundError(ResponseError):
    pass


class CFDIInvalidError(ResponseError):
    pass
