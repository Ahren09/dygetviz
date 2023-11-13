"""CLI commands for visualization."""

import argparse
import logging
import sys
import os.path as osp

# Add parent directory to path for imports
sys.path.insert(0, osp.join(osp.dirname(__file__), '..', '..'))

from dygetviz.utils.utils_logging import configure_default_logging
from dygetviz.utils.utils_misc import project_setup

configure_default_logging()
logger = logging.getLogger(__name__)


def visualize_embeddings():
    """Main entry point for embedding visualization."""
    parser = argparse.ArgumentParser(description='Visualize dynamic graph embeddings')
    parser.add_argument('--dataset_name', type=str, required=True,
                        help='Name of the dataset')
    parser.add_argument('--model', type=str, default='GConvGRU',
                        help='Model used for embedding generation')
    parser.add_argument('--port', type=int, default=8050,
                        help='Port for the visualization server')
    parser.add_argument('--debug', action='store_true',
                        help='Run in debug mode')
    parser.add_argument('--host', type=str, default='127.0.0.1',
                        help='Host for the visualization server')
    
    args = parser.parse_args()
    project_setup()
    
    logger.info(f"Starting visualization for dataset: {args.dataset_name}")
    logger.info(f"Model: {args.model}, Port: {args.port}")
    
    # Import and run the visualization
    from dygetviz.visualization.dash_app import create_dash_app
    app = create_dash_app(args)
    app.run_server(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    visualize_embeddings()