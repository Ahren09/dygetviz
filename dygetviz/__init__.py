"""DygETViz: Dynamic Graph Embedding Trajectory Visualization.

A Python package for visualizing dynamic graph neural networks (DGNNs) 
and dynamic graph embedding trajectories.
"""

__version__ = "0.1.0"
__author__ = "DygETViz Team"

# Core functionality imports
from . import data
from . import models
from . import embeddings
from . import visualization
from . import utils
from . import cli

# Key functions for easy access
from .data import load_data, load_data_dtdg
from .models import RecurrentGCN
from .utils import project_setup, configure_default_logging
try:
    from .visualization import create_dash_app
except ImportError:
    def create_dash_app(*args, **kwargs):
        raise ImportError("Visualization dependencies not installed. Install with: pip install dash plotly")

__all__ = [
    # Modules
    'data',
    'models', 
    'embeddings',
    'visualization',
    'utils',
    'cli',
    
    # Key functions
    'load_data',
    'load_data_dtdg',
    'RecurrentGCN',
    'project_setup',
    'configure_default_logging',
    'create_dash_app'
]