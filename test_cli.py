"""Test CLI functionality without actually running the commands."""

import sys
import os.path as osp

# Add current directory to path for imports
sys.path.insert(0, osp.dirname(__file__))

def test_cli_imports():
    """Test that CLI commands can be imported."""
    try:
        from dygetviz.cli.generate import generate_embeddings
        from dygetviz.cli.visualize import visualize_embeddings  
        from dygetviz.cli.serve import serve_dashboard
        
        print("✓ CLI imports successful")
        print("Available CLI commands:")
        print("  - dygetviz-generate: Generate embeddings")
        print("  - dygetviz-visualize: Visualize embeddings")
        print("  - dygetviz-serve: Serve dashboard")
        return True
    except Exception as e:
        print(f"✗ CLI import failed: {e}")
        return False

def test_package_installation_ready():
    """Test that package is ready for installation."""
    try:
        # Check setup.py exists
        assert osp.exists("setup.py"), "setup.py not found"
        
        # Check requirements.txt exists
        assert osp.exists("requirements.txt"), "requirements.txt not found"
        
        # Check main package structure
        assert osp.exists("dygetviz/__init__.py"), "Main package __init__.py not found"
        assert osp.exists("dygetviz/cli"), "CLI module not found"
        assert osp.exists("dygetviz/data"), "Data module not found"
        assert osp.exists("dygetviz/models"), "Models module not found"
        assert osp.exists("dygetviz/embeddings"), "Embeddings module not found"
        assert osp.exists("dygetviz/visualization"), "Visualization module not found"
        assert osp.exists("dygetviz/utils"), "Utils module not found"
        
        # Check examples and tests
        assert osp.exists("examples"), "Examples directory not found"
        assert osp.exists("tests"), "Tests directory not found"
        
        print("✓ Package structure ready for installation")
        return True
    except Exception as e:
        print(f"✗ Package structure check failed: {e}")
        return False

def main():
    """Run CLI tests."""
    print("Testing DygETViz CLI and Installation Readiness")
    print("=" * 60)
    
    tests = [
        test_cli_imports,
        test_package_installation_ready
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"CLI Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 DygETViz package is ready for use and installation!")
        print("\nNext steps:")
        print("1. Install in development mode: pip install -e .")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Use CLI commands: dygetviz-generate, dygetviz-visualize, dygetviz-serve")
        print("4. Import in Python: import dygetviz")
    else:
        print("❌ Some CLI tests failed.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)