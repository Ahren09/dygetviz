"""Basic usage example for DygETViz package."""

import sys
import os.path as osp

# Add parent directory to path for imports
sys.path.insert(0, osp.join(osp.dirname(__file__), '..'))

import dygetviz
from dygetviz.utils import project_setup, configure_default_logging


def main():
    """Basic usage example."""
    print(f"DygETViz version: {dygetviz.__version__}")
    
    # Setup project environment
    configure_default_logging()
    project_setup()
    
    print("Package setup completed successfully!")
    
    # Example: Try to load a dataset
    try:
        from dygetviz.data import load_data
        print("Data loading functions available")
        
        # Try loading a simple dataset (this may fail if dataset doesn't exist)
        # data = load_data("chickenpox", False)
        # print(f"Data loaded: {type(data)}")
        
    except Exception as e:
        print(f"Data loading failed (expected for missing datasets): {e}")
    
    # Example: Check model availability
    try:
        from dygetviz.models import RecurrentGCN, MODEL2CLASS
        print(f"Available models: {list(MODEL2CLASS.keys())}")
        
    except Exception as e:
        print(f"Model loading failed: {e}")
    
    # Example: Check CLI availability
    try:
        from dygetviz.cli import generate_embeddings, visualize_embeddings
        print("CLI functions available")
        
    except Exception as e:
        print(f"CLI loading failed: {e}")
    
    print("Basic usage example completed!")


if __name__ == "__main__":
    main()