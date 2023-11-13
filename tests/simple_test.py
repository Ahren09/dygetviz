"""Simple test script without pytest dependency."""

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
        print("✓ Main package import test passed")
        return True
    except Exception as e:
        print(f"✗ Main package import test failed: {e}")
        return False


def test_submodule_imports():
    """Test that all main submodules can be imported."""
    try:
        import dygetviz.data
        import dygetviz.models
        import dygetviz.embeddings
        import dygetviz.visualization
        import dygetviz.utils
        import dygetviz.cli
        print("✓ Submodule import test passed")
        return True
    except Exception as e:
        print(f"✗ Submodule import test failed: {e}")
        return False


def test_key_functions():
    """Test that key functions are available."""
    try:
        from dygetviz.data import load_data, load_data_dtdg
        from dygetviz.models import RecurrentGCN, MODEL2CLASS
        from dygetviz.utils import project_setup, configure_default_logging
        from dygetviz.cli import generate_embeddings, visualize_embeddings, serve_dashboard
        from dygetviz.embeddings import train_dynamic_graph_embeds, save_embeddings
        
        assert callable(load_data)
        assert callable(load_data_dtdg)
        assert RecurrentGCN is not None
        assert isinstance(MODEL2CLASS, dict)
        assert callable(project_setup)
        assert callable(configure_default_logging)
        assert callable(generate_embeddings)
        assert callable(visualize_embeddings)
        assert callable(serve_dashboard)
        assert callable(train_dynamic_graph_embeds)
        assert callable(save_embeddings)
        
        print("✓ Key functions test passed")
        return True
    except Exception as e:
        print(f"✗ Key functions test failed: {e}")
        return False


def test_package_structure():
    """Test that package structure is correct."""
    try:
        import dygetviz
        
        # Check that all expected modules are available
        expected_modules = ['data', 'models', 'embeddings', 'visualization', 'utils', 'cli']
        
        for module_name in expected_modules:
            module = getattr(dygetviz, module_name)
            assert module is not None
        
        print("✓ Package structure test passed")
        return True
    except Exception as e:
        print(f"✗ Package structure test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("Running DygETViz Package Tests")
    print("=" * 50)
    
    tests = [
        test_main_package_import,
        test_submodule_imports,
        test_key_functions,
        test_package_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Package is ready to use.")
        return True
    else:
        print("❌ Some tests failed. Check the output above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)