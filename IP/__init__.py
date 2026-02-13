# IP Protocol Package
# Orchestr8 v3.0
# This module exports core components for the plugin architecture.

from pathlib import Path

# Package metadata
__version__ = "3.0.0"
__package_name__ = "IP"

# Core module paths for verification
_IP_DIR = Path(__file__).parent
CORE_MODULE_PATHS = {
    "orchestr8.py": _IP_DIR.parent / "orchestr8.py",
    "louis_core.py": _IP_DIR / "louis_core.py",
    "carl_core.py": _IP_DIR / "carl_core.py",
    "connie.py": _IP_DIR / "connie.py",
}

def verify_structure() -> dict:
    """Verify IP Protocol directory structure integrity."""
    ip_dir = _IP_DIR
    results = {
        "ip_dir": ip_dir.exists(),
        "plugins_dir": (ip_dir / "plugins").exists(),
        "modules": {}
    }
    for module_name, module_path in CORE_MODULE_PATHS.items():
        results["modules"][module_name] = module_path.exists()
    return results
