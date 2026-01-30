"""
innov8 module for Jupyter experimental/innovation platform integration.

This module implements the Jupyter wrapper following the orchestr8 (Newelle) pattern,
providing complete experimental functionality within the Maestro workspace.
"""

from .adapter import *

__all__ = ['get_version', 'health_check', 'create_session', 'create_notebook', 
           'open_notebook', 'save_notebook', 'execute_cell', 'add_cell',
           'delete_cell', 'get_notebook_content', 'set_cell_content',
           'list_kernels', 'start_kernel', 'stop_kernel', 'restart_kernel']
