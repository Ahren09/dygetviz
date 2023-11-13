"""CLI commands for serving dashboards."""

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


def serve_dashboard():
    """Main entry point for serving dashboard."""
    parser = argparse.ArgumentParser(description='Serve dynamic graph visualization dashboard')
    parser.add_argument('--dataset_name', type=str, required=True,
                        help='Name of the dataset')
    parser.add_argument('--model', type=str, default='GConvGRU',
                        help='Model used for embedding generation')
    parser.add_argument('--port', type=int, default=8052,
                        help='Port for the dashboard server')
    parser.add_argument('--host', type=str, default='127.0.0.1',
                        help='Host for the dashboard server')
    parser.add_argument('--wholeplots', action='store_true',
                        help='Use wholeplots mode')
    
    args = parser.parse_args()
    project_setup()
    
    logger.info(f"Starting dashboard server for dataset: {args.dataset_name}")
    logger.info(f"Model: {args.model}, Port: {args.port}")
    
    # Import and run the appropriate server
    if args.wholeplots:
        from dygetviz.visualization.dash_server_wholeplots import create_server_app
    else:
        from dygetviz.visualization.dash_server import create_server_app
    
    app = create_server_app(args)
    app.run_server(host=args.host, port=args.port, debug=False)


if __name__ == '__main__':
    serve_dashboard()