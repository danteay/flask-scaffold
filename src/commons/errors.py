"""Custom error definitions"""


class HandlerError(Exception):
    """
    Generic handler error
    :param code: HTTP status code
    :param message: Error message
    :param errors: additional errors
    """

    def __init__(
        self,
        code: int,
        message: str,
        description: str = None,
        errors=None,
        root_causes: (str, list, dict) = None
    ):
        super().__init__(message, errors)

        self.message = message
        self.description = "Unexpected error" if description is None else description
        self.root_causes = root_causes
        self.code = code

    def get_message(self):
        """Get error message"""
        return self.message

    def get_code(self):
        """Get error code"""
        return self.code

    def get_description(self):
        """Return error description"""
        return self.description

    def get_root_causes(self):
        """Return"""
        return self.root_causes


class SchemaError(HandlerError):
    """JSON Schema validation error"""

    def __init__(self, errors):
        super().__init__(code=400, message="bad-request", errors=errors)
        self.description = "Schema validation error"
        self.root_causes = [{"error": errors.args[0].split(":  ")[0]}]


class InvalidPriceTypeError(HandlerError):
    """JSON Schema validation error"""

    def __init__(self, errors=None, root_causes=None):
        super().__init__(code=400, message="invalid-price-name", errors=errors)
        self.description = "Can't find the specified price name"
        self.root_causes = root_causes


class DiscountFieldError(HandlerError):
    """JSON Schema validation error"""

    def __init__(self, errors=None, root_causes=None):
        super().__init__(code=500, message="discount-field-error", errors=errors)
        self.description = "Error on discount configuration"
        self.root_causes = root_causes


class ConfigurationError(Exception):
    """Configuration loading error"""
