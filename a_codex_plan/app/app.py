"""a_codex_plan application entry point."""

import marimo

# Import modules for use in cells
from app.modules import _state, _services, _handlers

# Create the marimo app
app = marimo.App(
    width="compact",
)


@app.cell
def __title():
    """
    Title cell - displays the app header.
    """
    import marimo as mo

    return mo.md("# a_codex_plan")


@app.cell
def __init_state():
    """
    Initialize application state.
    """
    from app.modules._state import app_state

    return app_state


@app.cell
def __services():
    """
    Initialize services.
    """
    from app.modules._services import get_services

    services = get_services()
    return services


if __name__ == "__main__":
    # Allow running as: python -c "from app import app; print('OK')"
    print("OK")
