"""
cre8 module for GIMP creative image editor integration.

This module implements the GIMP wrapper following the orchestr8 (Newelle) pattern,
providing complete creative functionality within the Maestro workspace.
"""

from .adapter import *

__all__ = ['get_version', 'health_check', 'create_session', 'create_image', 
           'open_image', 'save_image', 'export_image', 'get_image_info',
           'close_image', 'list_open_images', 'apply_filter', 'resize_image',
           'crop_image', 'rotate_image', 'adjust_colors', 'add_layer']
