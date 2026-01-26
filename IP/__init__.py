# IP Protocol Package
# Orchestr8 v3.0 - The Fortress Factory
# This module exports core components for the plugin architecture.

from pathlib import Path

# Package metadata
__version__ = "3.0.0"
__package_name__ = "IP"

# Core module paths for verification
CORE_MODULES = [
    "orchestr8_app.py",
    "louis_core.py",
    "carl_core.py",
    "connie.py"
]

def verify_structure() -> dict:
    """Verify IP Protocol directory structure integrity."""
    ip_dir = Path(__file__).parent
    results = {
        "ip_dir": ip_dir.exists(),
        "plugins_dir": (ip_dir / "plugins").exists(),
        "modules": {}
    }
    for module in CORE_MODULES:
        results["modules"][module] = (ip_dir / module).exists()
    return results
