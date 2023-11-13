"""Data handling modules for dynamic graph datasets."""

from .dataloader import load_data, load_data_dtdg
from .dygetviz_dataset import DyGETVizDataset

try:
    from .chickenpox import ChickenpoxDataset
    from .static_graph_static_signal import StaticGraphStaticSignal
except ImportError:
    # These modules might not exist or have import issues
    pass

__all__ = [
    'load_data',
    'load_data_dtdg', 
    'DyGETVizDataset'
]