"""Application state management using marimo's mo.state() pattern."""

import marimo as mo


def create_app_state():
    """
    Create and initialize application state.

    Returns a dict-like object with state variables.
    """
    state = {
        # Example state fields
        "initialized": False,
        "data": None,
        "config": {},
        "user": None,
        # Add more state variables as needed
    }
    return state


# Module-level state accessor
# Usage: from app.modules._state import app_state
#        app_state["key"] = value
#        value = app_state.get("key")
app_state = mo.state({})


def get_state(key: str, default=None):
    """
    Get a state value.

    Args:
        key: The state key to retrieve
        default: Default value if key doesn't exist

    Returns:
        The state value or default
    """
    return app_state.get(key, default)


def set_state(key: str, value) -> None:
    """
    Set a state value.

    Args:
        key: The state key to set
        value: The value to store
    """
    app_state[key] = value


def reset_state() -> None:
    """Reset all state to defaults."""
    global app_state
    app_state = mo.state({})
