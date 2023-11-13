"""Utility functions and helpers for DygETViz."""

from .utils_misc import project_setup, set_seed
from .utils_logging import configure_default_logging
from .utils_data import get_modified_time_of_file, read_markdown_into_html, parse_contents
from .utils_visual import get_colors

try:  
    from .utils_training import get_training_args
except ImportError:
    # This might not exist yet or have dependency issues
    def get_training_args(*args, **kwargs):
        return None

__all__ = [
    'project_setup',
    'set_seed',
    'configure_default_logging',
    'get_modified_time_of_file',
    'read_markdown_into_html', 
    'parse_contents',
    'get_colors'
]