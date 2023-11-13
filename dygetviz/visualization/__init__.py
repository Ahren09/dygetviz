"""Visualization components for dynamic graph neural networks."""

try:
    from .dash_app import create_dash_app
    HAS_DASH_APP = True
except ImportError:
    HAS_DASH_APP = False
    def create_dash_app(*args, **kwargs):
        raise ImportError("Dash dependencies not installed. Install with: pip install dash plotly")

try:
    from .dash_server import create_server_app
    from .dash_server_wholeplots import create_server_wholeplots_app
except ImportError:
    # These modules might not exist yet
    pass

__all__ = [
    'create_dash_app'
] if HAS_DASH_APP else []