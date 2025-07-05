class CatalogueNotFoundError(Exception):
    """Raised when a catalogue entry is not found."""
    pass

class InvalidCatalogueInputError(Exception):
    """Raised when input data is invalid."""
    pass

class DatabaseConnectionError(Exception):
    """Raised when the database connection fails."""
    pass

class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass

class InvalidCredentialsError(Exception):
    """Raised when login credentials are invalid."""
    pass

class CatalogueAlreadyExistsError(Exception):
    """Raised when trying to create a catalogue that already exists."""
    pass