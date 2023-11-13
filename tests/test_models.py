"""Test model functionality."""

import pytest
import torch
import sys
import os.path as osp

# Add parent directory to path for imports
sys.path.insert(0, osp.join(osp.dirname(__file__), '..'))


class TestRecurrentGCN:
    """Test RecurrentGCN model functionality."""
    
    def test_recurrent_gcn_import(self):
        """Test that RecurrentGCN can be imported."""
        from dygetviz.models import RecurrentGCN
        assert RecurrentGCN is not None
    
    def test_model2class_dict(self):
        """Test that MODEL2CLASS dictionary exists and contains expected models."""
        from dygetviz.models import MODEL2CLASS
        assert isinstance(MODEL2CLASS, dict)
        assert "GConvGRU" in MODEL2CLASS
    
    def test_recurrent_gcn_initialization(self):
        """Test RecurrentGCN model initialization."""
        try:
            from dygetviz.models import RecurrentGCN
            
            # Test basic initialization
            model = RecurrentGCN(
                model="GConvGRU",
                node_features=10,
                hidden_dim=64,
                device="cpu"
            )
            
            assert model is not None
            assert isinstance(model, torch.nn.Module)
            
        except Exception as e:
            # If torch_geometric_temporal is not available, skip
            if "torch_geometric_temporal" in str(e):
                pytest.skip("torch_geometric_temporal not available")
            else:
                pytest.fail(f"Unexpected error in model initialization: {e}")
    
    def test_recurrent_gcn_forward_pass(self):
        """Test RecurrentGCN forward pass with dummy data."""
        try:
            from dygetviz.models import RecurrentGCN
            
            model = RecurrentGCN(
                model="GConvGRU",
                node_features=10,
                hidden_dim=64,
                device="cpu"
            )
            
            # Create dummy input data
            num_nodes = 100
            x = torch.randn(num_nodes, 10)  # Node features
            edge_index = torch.randint(0, num_nodes, (2, 200))  # Random edges
            
            # Test forward pass
            output = model(x, edge_index)
            
            assert output is not None
            assert output.shape[0] == num_nodes
            assert output.shape[1] == 64  # hidden_dim
            
        except Exception as e:
            if "torch_geometric_temporal" in str(e):
                pytest.skip("torch_geometric_temporal not available")
            else:
                pytest.fail(f"Unexpected error in forward pass: {e}")


if __name__ == "__main__":
    pytest.main([__file__])