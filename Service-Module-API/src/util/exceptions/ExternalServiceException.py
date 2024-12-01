class ExternalServiceException(Exception):

    def __init__(self, message: str, service_name: str = None, status_code: int = None, details: dict = None):
        """
        Initialize the ExternalServiceException.
        
        Args:
            message (str): The error message.
            service_name (str, optional): The name of the external service.
            status_code (int, optional): The HTTP status code returned by the service.
            details (dict, optional): Additional details about the error.
        """
        self.service_name = service_name
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self._build_message(message))

    def _build_message(self, message: str) -> str:
        """
        Build a detailed error message including service name and status code.
        
        Args:
            message (str): The base error message.
        
        Returns:
            str: The formatted error message.
        """
        error_message = f"ExternalServiceException: {message}"
        if self.service_name:
            error_message += f" | Service: {self.service_name}"
        if self.status_code:
            error_message += f" | Status Code: {self.status_code}"
        if self.details:
            error_message += f" | Details: {self.details}"
        return error_message

    def __str__(self):
        return self._build_message(super().__str__())
