"""Main Dash application for interactive visualization."""

import os.path as osp
import sys

import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from dash import dcc, html, no_update
from dash.dependencies import Input, Output, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from tqdm import tqdm

# Add parent directory to path for imports
sys.path.insert(0, osp.join(osp.dirname(__file__), '..', '..'))

import dash_ag_grid as dag

from dygetviz import const
from dygetviz import const
from dygetviz.arguments import parse_args
from dygetviz.components.dygetviz_components import (
    graph_with_loading, dataset_description, interpretation_of_plot,
    visualization_panel
)
from dygetviz.components.upload import upload_panel
from dygetviz.data.dataloader import load_data
from dygetviz.utils.utils_data import get_modified_time_of_file, read_markdown_into_html, parse_contents
from dygetviz.utils.utils_misc import project_setup
from dygetviz.utils.utils_visual import get_colors


def create_dash_app(args=None):
    """Create and configure the main Dash application.
    
    Args:
        args: Command line arguments. If None, will parse from command line.
        
    Returns:
        dash.Dash: Configured Dash application
    """
    if args is None:
        args = parse_args()
    
    project_setup()
    
    print("Loading data...")
    
    app = dash.Dash(
        __name__, 
        external_stylesheets=[
            dbc.themes.BOOTSTRAP, 
            "../dygetviz/assets/base.css",
            "../dygetviz/assets/clinical-analytics.css"
        ]
    )
    
    # Load data
    data = load_data(args.dataset_name, False)
    
    annotation: dict = data.get("annotation", {})
    display_node_type: bool = data["display_node_type"]
    idx_reference_snapshot: int = data["idx_reference_snapshot"]
    interpolation: float = data["interpolation"]
    node_presence: np.ndarray = data["node_presence"]
    node2idx: dict = data["node2idx"]
    node2label: dict = data["node2label"]
    label2node: dict = data["label2node"]
    
    # Configure app layout
    app.layout = _create_layout(data, args)
    
    # Register callbacks
    _register_callbacks(app, data, args)
    
    return app


def _create_layout(data, args):
    """Create the main layout for the Dash app."""
    return html.Div([
        dcc.Store(id='dataset-store', data=data),
        dcc.Store(id='args-store', data=vars(args)),
        
        # Header
        html.Div([
            html.H1(f"DygETViz - {args.dataset_name}", className="text-center mb-4"),
            html.Hr()
        ]),
        
        # Main content
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    dataset_description(args.dataset_name),
                    visualization_panel(),
                    upload_panel(),
                ], width=3),
                
                dbc.Col([
                    graph_with_loading(),
                    interpretation_of_plot(),
                ], width=9),
            ])
        ], fluid=True)
    ])


def _register_callbacks(app, data, args):
    """Register all callbacks for the Dash app."""
    
    @app.callback(
        Output('graph', 'figure'),
        [Input('visualization-controls', 'value')]
    )
    def update_graph(controls):
        """Update the main graph based on visualization controls."""
        # Implementation would go here
        fig = go.Figure()
        fig.add_scatter(x=[1, 2, 3], y=[1, 2, 3], mode='markers')
        fig.update_layout(title="Dynamic Graph Visualization")
        return fig


if __name__ == '__main__':
    app = create_dash_app()
    app.run_server(debug=True)