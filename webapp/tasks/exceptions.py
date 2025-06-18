class NotFound(Exception):
    """
    Custom exception to handle DoesNotExist exceptions.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"NotFound: {self.message}"

    def __repr__(self):
        return f"NotFound({self.message!r})"
