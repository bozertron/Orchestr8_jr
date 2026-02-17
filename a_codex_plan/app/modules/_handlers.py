"""Event and action handlers pattern."""

import marimo as mo
from typing import Callable, Any


class EventHandler:
    """
    Base class for event handlers.
    """

    def __init__(self, name: str):
        self.name = name
        self._callbacks = []

    def register(self, callback: Callable):
        """Register a callback function."""
        self._callbacks.append(callback)

    def trigger(self, *args, **kwargs) -> list:
        """Trigger all registered callbacks."""
        results = []
        for callback in self._callbacks:
            try:
                result = callback(*args, **kwargs)
                results.append(result)
            except Exception as e:
                results.append({"error": str(e)})
        return results


class ClickHandler(EventHandler):
    """Handler for click events."""

    def __init__(self, name: str = "click"):
        super().__init__(name)

    def on_click(self, *args, **kwargs):
        """Handle click event."""
        return self.trigger(*args, **kwargs)


class DataHandler(EventHandler):
    """Handler for data-related events."""

    def __init__(self, name: str = "data"):
        super().__init__(name)

    def load(self, source: str) -> dict:
        """Handle data load request."""
        return self.trigger(source)

    def process(self, data: Any) -> dict:
        """Handle data processing request."""
        return self.trigger(data)


# Global handler instances
_click_handler = ClickHandler()
_data_handler = DataHandler()


def get_click_handler() -> ClickHandler:
    """Get the global click handler."""
    return _click_handler


def get_data_handler() -> DataHandler:
    """Get the global data handler."""
    return _data_handler


# Example handler functions


def handle_button_click(button_id: str) -> str:
    """
    Handle button click events.

    Args:
        button_id: Unique identifier for the clicked button

    Returns:
        Status message
    """
    return f"Button {button_id} clicked"


def handle_data_load(source: str) -> dict:
    """
    Handle data load requests.

    Args:
        source: Data source identifier

    Returns:
        Load result dict
    """
    return {"status": "loading", "source": source}


def handle_form_submit(form_data: dict) -> dict:
    """
    Handle form submission.

    Args:
        form_data: Submitted form data

    Returns:
        Submission result
    """
    return {"status": "submitted", "data": form_data}
