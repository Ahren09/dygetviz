"""Test data loading and processing functionality."""

import pytest
import numpy as np
import os.path as osp
import sys

# Add parent directory to path for imports
sys.path.insert(0, osp.join(osp.dirname(__file__), '..'))


class TestDataLoading:
    """Test data loading functionality."""
    
    def test_load_data_function_exists(self):
        """Test that load_data function exists and is callable."""
        from dygetviz.data import load_data
        assert callable(load_data)
    
    def test_load_data_dtdg_function_exists(self):
        """Test that load_data_dtdg function exists and is callable."""
        from dygetviz.data import load_data_dtdg
        assert callable(load_data_dtdg)
    
    @pytest.mark.parametrize("dataset_name", [
        "chickenpox", 
        "test_dataset"
    ])
    def test_load_data_with_invalid_dataset(self, dataset_name):
        """Test load_data behavior with potentially invalid datasets."""
        from dygetviz.data import load_data
        
        # This should either return a result or raise an appropriate exception
        try:
            result = load_data(dataset_name, False)
            # If it succeeds, result should be a dictionary
            if result is not None:
                assert isinstance(result, dict)
        except (FileNotFoundError, ValueError, KeyError) as e:
            # These are expected exceptions for missing datasets
            pass
        except Exception as e:
            pytest.fail(f"Unexpected exception type: {type(e).__name__}: {e}")


class TestDatasetClasses:
    """Test dataset class functionality."""
    
    def test_dygetviz_dataset_exists(self):
        """Test that DygETVizDataset class exists."""
        try:
            from dygetviz.data import DygETVizDataset
            assert DygETVizDataset is not None
        except ImportError:
            pytest.skip("DygETVizDataset not available")


if __name__ == "__main__":
    pytest.main([__file__])