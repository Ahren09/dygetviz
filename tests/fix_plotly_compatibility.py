"""Fix Plotly compatibility issues in cached JSON files.

This script fixes the deprecated 'heatmapgl' property in cached visualization JSON files
by replacing it with 'heatmap' to maintain compatibility with newer Plotly versions.
"""

import os
import os.path as osp
import json
import glob


def fix_heatmapgl_in_file(file_path):
    """Fix heatmapgl property in a single JSON file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        if 'heatmapgl' in content:
            print(f"Fixing {file_path}...")
            
            # Replace deprecated property
            fixed_content = content.replace('"heatmapgl"', '"heatmap"')
            
            # Validate that it's still valid JSON
            json.loads(fixed_content)
            
            # Write back the fixed content
            with open(file_path, 'w') as f:
                f.write(fixed_content)
            
            print(f"✓ Fixed {file_path}")
            return True
        else:
            print(f"✓ {file_path} already compatible")
            return False
            
    except Exception as e:
        print(f"✗ Error fixing {file_path}: {e}")
        return False


def fix_all_json_files(base_dir="outputs"):
    """Fix all JSON files in the outputs directory."""
    if not osp.exists(base_dir):
        print(f"Directory {base_dir} not found. Skipping fix.")
        return
    
    # Find all JSON files in outputs directory
    json_pattern = osp.join(base_dir, "**", "*.json")
    json_files = glob.glob(json_pattern, recursive=True)
    
    if not json_files:
        print("No JSON files found in outputs directory.")
        return
    
    print(f"Found {len(json_files)} JSON files to check...")
    
    fixed_count = 0
    for json_file in json_files:
        if fix_heatmapgl_in_file(json_file):
            fixed_count += 1
    
    print(f"\n🎉 Fixed {fixed_count} out of {len(json_files)} files")
    if fixed_count > 0:
        print("All cached visualizations are now compatible with current Plotly version!")


def main():
    """Main function to fix Plotly compatibility issues."""
    print("Fixing Plotly Compatibility Issues")
    print("=" * 50)
    print("This script fixes deprecated 'heatmapgl' properties in cached JSON files")
    print()
    
    # Change to the directory containing the script
    script_dir = osp.dirname(osp.abspath(__file__))
    os.chdir(script_dir)
    
    fix_all_json_files()
    
    print("\n" + "=" * 50)
    print("Plotly compatibility fix completed!")


if __name__ == "__main__":
    main()