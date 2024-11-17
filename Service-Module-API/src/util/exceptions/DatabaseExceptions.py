class EntityDoesNotExist(Exception):
    """
    Exception raised when an entity is not found in the database.
    
    Attributes:
        message (str): Custom error message for the exception.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message
