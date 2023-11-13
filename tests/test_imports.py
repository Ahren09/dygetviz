"""Test basic package imports to ensure package structure is correct."""

import pytest
import sys
import os.path as osp

# Add parent directory to path for imports
sys.path.insert(0, osp.join(osp.dirname(__file__), '..'))


def test_main_package_import():
    """Test that main package can be imported."""
    try:
        import dygetviz
        assert hasattr(dygetviz, '__version__')
        assert dygetviz.__version__ == "0.1.0"
    except ImportError as e:
        pytest.fail(f"Failed to import main package: {e}")


def test_submodule_imports():
    """Test that all main submodules can be imported."""
    try:
        import dygetviz.data
        import dygetviz.models
        import dygetviz.embeddings
        import dygetviz.visualization
        import dygetviz.utils
        import dygetviz.cli
    except ImportError as e:
        pytest.fail(f"Failed to import submodules: {e}")


def test_data_module_functions():
    """Test that key data functions are available."""
    try:
        from dygetviz.data import load_data, load_data_dtdg
        assert callable(load_data)
        assert callable(load_data_dtdg)
    except ImportError as e:
        pytest.fail(f"Failed to import data functions: {e}")


def test_models_module_classes():
    """Test that key model classes are available."""
    try:
        from dygetviz.models import RecurrentGCN, MODEL2CLASS
        assert RecurrentGCN is not None
        assert isinstance(MODEL2CLASS, dict)
    except ImportError as e:
        pytest.fail(f"Failed to import model classes: {e}")


def test_utils_module_functions():
    """Test that key utility functions are available.""" 
    try:
        from dygetviz.utils import project_setup, configure_default_logging
        assert callable(project_setup)
        assert callable(configure_default_logging)
    except ImportError as e:
        pytest.fail(f"Failed to import utility functions: {e}")


def test_cli_module_functions():
    """Test that CLI functions are available."""
    try:
        from dygetviz.cli import generate_embeddings, visualize_embeddings, serve_dashboard
        assert callable(generate_embeddings)
        assert callable(visualize_embeddings)
        assert callable(serve_dashboard)
    except ImportError as e:
        pytest.fail(f"Failed to import CLI functions: {e}")


def test_embedding_module_functions():
    """Test that embedding functions are available."""
    try:
        from dygetviz.embeddings import train_dynamic_graph_embeds, save_embeddings
        assert callable(train_dynamic_graph_embeds)
        assert callable(save_embeddings)
    except ImportError as e:
        pytest.fail(f"Failed to import embedding functions: {e}")


if __name__ == "__main__":
    pytest.main([__file__])