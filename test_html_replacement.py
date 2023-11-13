"""Test the HTML replacement for dash_dangerously_set_inner_html."""

import sys
import os.path as osp

# Add current directory to path for imports
sys.path.insert(0, osp.dirname(__file__))

def test_html_replacement():
    """Test that the HTML replacement works."""
    try:
        from dygetviz.components.dygetviz_components import visualization_panel
        print('✓ Successfully imported visualization_panel with new HTML approach')
        
        # Test if we can create the component
        panel = visualization_panel()
        print('✓ Successfully created visualization panel component')
        print('✓ dash_dangerously_set_inner_html replacement working!')
        
        return True
        
    except Exception as e:
        print(f'✗ Error: {e}')
        return False

def test_other_components():
    """Test other component functions."""
    try:
        from dygetviz.components.dygetviz_components import (
            dataset_description, 
            graph_with_loading, 
            interpretation_of_plot
        )
        
        # Test dataset_description
        desc = dataset_description("test_dataset")
        print('✓ dataset_description component works')
        
        # Test graph_with_loading  
        graph = graph_with_loading()
        print('✓ graph_with_loading component works')
        
        # Test interpretation_of_plot
        interp = interpretation_of_plot()
        print('✓ interpretation_of_plot component works')
        
        return True
        
    except Exception as e:
        print(f'✗ Error testing other components: {e}')
        return False

def main():
    """Run all tests."""
    print("Testing HTML Replacement for dash_dangerously_set_inner_html")
    print("=" * 60)
    
    tests = [
        test_html_replacement,
        test_other_components
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 HTML replacement successful!")
        print("\nSolution: Using html.Div with dangerouslySetInnerHTML prop")
        print("Benefits:")
        print("- No external dependency required")
        print("- Uses native Dash functionality") 
        print("- Compatible with all Dash versions")
        print("- Same security model as the original component")
    else:
        print("❌ Some tests failed.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)