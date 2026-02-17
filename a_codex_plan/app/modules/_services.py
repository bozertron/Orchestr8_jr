"""Service instantiation and management pattern."""


class BaseService:
    """Base class for all services."""

    def __init__(self, config: dict = None):
        self.config = config or {}
        self._initialized = False

    def initialize(self):
        """Initialize the service."""
        self._initialized = True

    def is_initialized(self) -> bool:
        return self._initialized


class DataService(BaseService):
    """Service for data operations."""

    def __init__(self, config: dict = None):
        super().__init__(config)
        self._data = []

    def load_data(self, source: str):
        """Load data from source."""
        # Placeholder implementation
        self._data = [{"source": source, "items": []}]
        return self._data

    def get_data(self):
        """Retrieve loaded data."""
        return self._data


class ConfigService(BaseService):
    """Service for configuration management."""

    def __init__(self, config: dict = None):
        super().__init__(config)
        self._config = config or {}

    def get(self, key: str, default=None):
        """Get a config value."""
        return self._config.get(key, default)

    def set(self, key: str, value):
        """Set a config value."""
        self._config[key] = value


# Service registry
_services = {}


def get_services() -> dict:
    """
    Get or create all services.

    Returns a dict of service instances.
    """
    global _services

    if not _services:
        # Initialize services on first access
        _services = {
            "data": DataService(),
            "config": ConfigService(),
        }
        # Initialize all services
        for service in _services.values():
            service.initialize()

    return _services


def get_service(name: str) -> BaseService:
    """
    Get a specific service by name.

    Args:
        name: Service name ('data', 'config', etc.)

    Returns:
        Service instance
    """
    services = get_services()
    return services.get(name)


def reset_services() -> None:
    """Reset all services (useful for testing)."""
    global _services
    _services = {}
