"""Run the Dash server to interactively add nodes to the visualization.
Plot using [Dash](https://dash.plotly.com/)
"""

import os.path as osp

import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from dash import dcc, html, no_update
from dash.dependencies import Input, Output, State
# import dash_mantine_components as dmc  # Disabled due to upload panel being disabled
# from dash_iconify import DashIconify  # Disabled due to upload panel being disabled
from tqdm import tqdm

# import dash_ag_grid as dag  # Disabled due to upload panel being disabled

import const
import const
from arguments import parse_args
from components.dygetviz_components import graph_with_loading, dataset_description, interpretation_of_plot, \
    visualization_panel
# from components.upload import upload_panel  # Disabled due to upload panel being disabled
from data.dataloader import load_data
from utils.utils_data import get_modified_time_of_file, read_markdown_into_html
from utils.utils_misc import project_setup
from utils.utils_visual import get_colors

print("Loading data...")

args = parse_args()
project_setup()
print("Start the app ...")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, "../dygetviz/assets/base.css",
                                                "../dygetviz/assets/clinical-analytics.css"])


data = load_data(args.dataset_name, False)

annotation: dict = data.get("annotation", {})
display_node_type: bool = data["display_node_type"]
idx_reference_snapshot: int = data["idx_reference_snapshot"]
interpolation: float = data["interpolation"]
node_presence: np.ndarray = data["node_presence"]
node2idx: dict = data["node2idx"]
node2label: dict = data["node2label"]
label2node: dict = data["label2node"]
label2name: dict = data["label2name"]
metadata_df: dict = data["metadata_df"]
num_nearest_neighbors: int = data["num_nearest_neighbors"]
perplexity: int = data["perplexity"]
plot_anomaly_labels: bool = data["plot_anomaly_labels"]
projected_nodes: np.ndarray = data["projected_nodes"]
reference_nodes: np.ndarray = data["reference_nodes"]
snapshot_names: list = data["snapshot_names"]
z = data["z"]

args = parse_args()

idx2node = {idx: node for node, idx in node2idx.items()}

visualization_name = f"{args.dataset_name}_{args.model}_{args.visualization_model}_perplex{perplexity}_nn{data['num_nearest_neighbors'][0]}_interpolation{interpolation}_snapshot{idx_reference_snapshot}"

print("Reading visualization cache...")

path = osp.join(args.visual_dir, f"Trajectory_{visualization_name}.json")

get_modified_time_of_file(path)

if args.debug:
    fig_cached = node2trace = None


else:
    try:
        fig_cached = pio.read_json(path)
    except ValueError as e:
        if 'heatmapgl' in str(e):
            print("⚠️  Found deprecated 'heatmapgl' in cached file. Attempting to fix...")
            # Read the JSON file and replace heatmapgl with heatmap
            with open(path, 'r') as f:
                json_content = f.read()
            
            # Replace deprecated property
            fixed_content = json_content.replace('"heatmapgl"', '"heatmap"')
            
            # Try to parse again with the fixed content
            import json
            fixed_data = json.loads(fixed_content)
            fig_cached = pio.from_json(json.dumps(fixed_data))
            
            # Optionally save the fixed version
            print("✓ Successfully fixed deprecated 'heatmapgl' property")
        else:
            raise e

    node2trace = {
        trace['name'].split(' ')[0]: trace for trace in fig_cached.data
    }

print("Getting candidate nodes ...")

if args.dataset_name in ["DGraphFin"]:
    nodes = [n for n, l in node2label.items() if l in [0, 1]]
else:
    nodes = list(node2idx.keys())

options = []

# If there are multiple node categories, we can display a distinct color family for each type of nodes
# NOTE: We specifically require that the first color palette is Blue (for normal nodes) and the second one is Red (for anomalous nodes)
if display_node_type:
    labels = sorted(list(label2node.keys()))
    label2palette = dict(zip(labels,
                             const.pure_color_palettes[:len(label2node)]))
    label2colors = {label: get_colors(12, label2palette[label])[::-1] for label
                    in labels}


else:
    # Otherwise, we use a single color family for all nodes. But the colors are very distinct
    label2colors = {
        0: get_colors(10, "Spectral")
    }

print("Adding categories to the dropdown menu ...")
options_categories = []

for label, nodes_li in label2node.items():
    options_categories.append({
        "label": html.Span(
            [
                "✨",
                html.Span(label, style={
                    'font-size': 15,
                    'padding-left': 10
                }),
            ], style={
                'align-items': 'center',
                'justify-content': 'center'
            }
        ),
        "value": label,
    })

print("Adding nodes to the dropdown menu ...")

options_nodes = []

for node, idx in node2idx.items():
    # Only add trajectories of projected or reference nodes
    if not node in projected_nodes:
        continue

    # For the DGraphFin dataset, the background nodes (label = 2 or 3) are not meaningful due to insufficient information. So we do not visualize them
    if display_node_type and args.dataset_name in [
        "DGraphFin"] and node2label.get(node) is None:
        print(f"\tIgnoring node {node} ...")
        continue

    if display_node_type:
        label = node2label[node]

        name = f"{node} ({label2name[label]})"

    else:
        name = node

    options_nodes.append({
        "label": html.Span(
            [
                html.Span(name, style={
                    'font-size': 15,
                    'padding-left': 10
                }),
            ], style={
                'align-items': 'center',
                'justify-content': 'center'
            }
        ),
        "value": node,  # Get a random node as the default value.
    })

options = options_categories + options_nodes

print("Reading plotly button explanations ...")
with open('dygetviz/static/Plotly_Button_Explanations.html', 'r') as file:
    plotly_button_explanations = file.read()

app.title = f"DyGetViz | {args.dataset_name}"


print("Reading dataset explanations ...")
dataset_descriptions = read_markdown_into_html(osp.join(args.data_dir, args.dataset_name, "data_descriptions.md"))


app.layout = html.Div(
    id="app-container",
    children=[
        html.Div(
            id="banner",
            className="banner",
            children=[
                # html.Img(src="https://brand.gatech.edu/sites/default/files/inline-images/GeorgiaTech_RGB.png"),
                # Title
                html.H1(f"DyGETViz",
                      className="text-center mb-4",
                    ),
                ],
        ),



        # Left column: node selection, dataset description, and interpretation of the plot
        html.Div(
            id="left-column",
            className="four columns",
            children=[dbc.Row([
                # Dropdown Row
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("Select trajectories:",
                                          className="form-label mb-2",
                                          id="note-trajectory",
                                          style={
                                              'font-weight': 'bold',
                                              'color': '#34495e',
                                              'width': '100%'
                                          }),
                            ],
                            className="right",
                            width=3,
                        ),
                        dbc.Col(
                            [
                                dcc.Dropdown(
                                    id='add-trajectory',
                                    options=options,
                                    value='',
                                    multi=True,
                                    placeholder="Select a node",
                                    style={
                                        'width': '100%'
                                    },
                                    clearable=True
                                )
                            ],
                            className="center mb-4",
                            # margin-bottom to give some space below
                            width=6

                        )
                    ],
                    className="text-center mb-4"
                    # margin-bottom to give some space below the row
                ),
                dbc.Row([


                    dataset_description(args.dataset_name),

                    interpretation_of_plot()

                    # This loads the dataset description from a markdown file.
                    # Archived
                    # html.Iframe(srcDoc=dataset_descriptions,
                    #             style={"width": "100%", "height": "500px"}),
                ]),

                dbc.Row([
                    html.H4(f"Panel", className="text-center"),

                    visualization_panel(),
                    # html.Iframe(srcDoc=plotly_button_explanations,
                    #             style={"width": "100%", "height": "500px"})
                ])
            ]),
        ]),

        # Right column: visualization panel


        

        html.Div(
            id="right-column",
            className="eight columns",
            children=[

                # The main dashboard
                graph_with_loading(),

                # Store the nodes in `trajectory_names`
                dcc.Store(
                    id='trajectory-names-store',
                    data=[]),

                dcc.Store(id="dataset-store", storage_type="local"),
                html.Div(
                    [
                        html.Div(
                            [
                                # upload_panel(),  # Disabled due to dash_mantine_components compatibility issues
                                html.Div("Upload panel disabled for compatibility"),
                            ],
                            style={"padding": "20px"}
                        ),
                    ],
                    style={"max-width": "1200px", "margin": "0 auto"}
                ),

            ]
        ),





        # dbc.Row([
        #     dbc.Col([
        #         html.Label("Change Trajectory Color:"),
        #         # Dropdown for selecting a node
        #         dcc.Dropdown(
        #             id='node-selector',
        #             options=[],
        #             value=nodes[0],
        #             style={
        #                 'width': '50%'
        #             },
        #         ),
        #
        #         # Store the nodes in `trajectory_names`
        #         dcc.Store(
        #             id='trajectory-names-store',
        #             data=[]
        #         ),
        #
        #         daq.ColorPicker(
        #             id='color-picker',
        #             label='Color Picker',
        #             size=328,
        #             value=dict(hex='#119DFF')
        #         ),
        #         html.Div(id='color-picker-output-1'),
        #         html.Button('Update Node Color', id='update-color-button',
        #                     n_clicks=0, className="me-2"),
        #     ])
        # ]),



    ])


def generate_node_profile(profile: pd.DataFrame):
    def f(x):
        ret = "<ul>"
        for field in x.index:
            ret += f"<li>{field}: {x[field]}</li>"
        ret += "</ul>"
        return ret

    profile['description'] = profile.apply(f, axis=1)
    return profile

def convert_scatter_to_scattergl(scatter):
    line = { "color": scatter.line.color, "dash": scatter.line.dash, "shape": scatter.line.shape, "width": scatter.line.width }
    marker = { "size": scatter.marker.size, 'symbol': scatter.marker.symbol}
    
    # Fix mode for background traces - if mode is 'markers+text' but no text, use just 'markers'
    mode = scatter.mode
    if mode == 'markers+text' and (not scatter.text or all(not t for t in scatter.text)):
        mode = 'markers'
    
    # Try using regular Scatter instead of Scattergl for better compatibility
    return go.Scatter(x=scatter.x, y=scatter.y, xaxis=scatter.xaxis, yaxis=scatter.yaxis, customdata=scatter.customdata,
                        hovertemplate=scatter.hovertemplate, hovertext=scatter.hovertext, legendgroup=scatter.legendgroup,
                        line= line, marker=marker, mode=mode, name=scatter.name, showlegend=scatter.showlegend,
                          selectedpoints=scatter.selectedpoints, text=scatter.text, textposition=scatter.textposition)

# List to keep track of current annotations
annotations = []


@app.callback(
    Output('dygetviz', 'figure'),
    Output('trajectory-names-store', 'data'),
    Input('add-trajectory', 'value'),
    Input('dygetviz', 'clickData'),
    State('dygetviz', 'figure'),
    # Input('update-color-button', 'n_clicks'),
    # State('node-selector', 'value'),
    # State('color-picker', 'value'),

)
def update_graph(trajectory_names, clickData, current_figure,
                 # do_update_color, selected_node, selected_color,
                 ):
    """

    :param trajectory_names: Names of the trajectories to be added into the visualization
    :param background_node_names:
    :param do_update_color:
    :param selected_node:
    :param selected_color:
    :param current_figure: figure from the previous update
    :return:
    """

    global annotations

    if not trajectory_names:
        trajectory_names = []

    ctx = dash.callback_context
    action_name = ctx.triggered[0]['prop_id'].split('.')[0]
    print(f"[Action]\t{action_name}")

    # This is the template for displaying metadata when hovering over a node

    fig = go.Figure()
    fig.update_layout(
        plot_bgcolor='white',
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False
        )
    )

    if current_figure is None:
        figure_name2trace = {}


    else:
        figure_name2trace = {trace['name']: trace for idx, trace in
                             enumerate(current_figure['data'])}

    def add_background():

        # Always add background trace
        trace = node2trace['background']
        print(f"Background trace type: {type(trace)}")
        # Convert to Scattergl for consistency
        trace = convert_scatter_to_scattergl(trace)
        print(f"Background trace after conversion: {type(trace)}")
        # Ensure marker is visible
        if hasattr(trace, 'marker'):
            trace.marker.update(
                size=8,  # Increase size
                opacity=0.8,  # Increase opacity
                color='#B2B2B2'  # Ensure color is set
            )
        print(f"Adding background trace with mode: {trace.mode}")
        # trace.hovertemplate = HOVERTEMPLATE
        fig.add_trace(trace)

        # Add anomaly labels if enabled
        if plot_anomaly_labels:
            trace = node2trace['anomaly']
            # Convert to Scattergl for consistency
            trace = convert_scatter_to_scattergl(trace)
            fig.add_trace(trace)

    def add_traces():
        for name, trace in figure_name2trace.items():
            if name not in {"background"}:
                fig.add_trace(trace)

    if action_name == '':
        """Launch the app for the first time. 
        
        Only add the background nodes
        """

        # In debug mode, we do not manipulate the figure. Only test the upload module
        if not args.debug:
            add_background()
            print(f"Initial figure has {len(fig.data)} traces:")
            for i, trace in enumerate(fig.data):
                print(f"  Trace {i}: {trace.name} (type: {type(trace)}, mode: {trace.mode})")
        return fig, trajectory_names

    elif action_name == 'add-trajectory':
        fig = go.Figure()
        fig.update_layout(
            plot_bgcolor='white',
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                showticklabels=False
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                showticklabels=False
            )
        )

        # Always add background first
        add_background()

        # Get existing trajectories (excluding background)
        existing_trajectories = {name: trace for name, trace in figure_name2trace.items() 
                               if name != "background"}

        print(f"Existing trajectories: {list(existing_trajectories.keys())}")

        # Add existing trajectories
        for name, trace in existing_trajectories.items():
            print(f"Adding existing trajectory: {name}")
            fig.add_trace(trace)

        # Add new trajectories
        new_trajectory_names = list(
            set(trajectory_names) - set(existing_trajectories.keys()))

        print(f"New search values:\t{new_trajectory_names}")
        
        # Track color index separately for new trajectories
        color_idx = len(existing_trajectories)
        
        for value in trajectory_names:
            if args.dataset_name == "DGraphFin" and node2label.get(
                    value) is None:
                print(f"Node {value} is a background node, so we ignore it.")
                continue

            # Skip if already added (existing trajectory)
            if value in existing_trajectories:
                continue

            # Add a new node
            if value in nodes:
                print(f"Processing node: {value}")
                trace = node2trace[value]
                print(f"Original trace type: {type(trace)}")
                trace = convert_scatter_to_scattergl(trace)
                print(f"Converted trace type: {type(trace)}")
                
                if display_node_type:
                    label = node2label[value]
                    color = label2colors[label][color_idx % len(label2colors[label])]
                    trace.line['color'] = color
                    print(f"\tAdd node:\t{value} ({label2name[label]}) with color {color}")

                else:
                    color = label2colors[0][color_idx % len(label2colors[0])]
                    trace.line['color'] = color
                    print(f"\tAdd node:\t{value} with color {color}")
                
                # Ensure line properties are set for trajectory visibility
                if hasattr(trace, 'line'):
                    trace.line.update(
                        width=3,  # Make line thicker
                    )
                    print(f"Set line properties: width={trace.line.width}")

                # Ensure the trace has proper mode and marker settings
                if hasattr(trace, 'mode'):
                    # For trajectory traces, use 'markers+lines' instead of 'markers+lines+text' if text is empty
                    if 'text' in trace.mode and (not trace.text or all(not t for t in trace.text)):
                        trace.mode = trace.mode.replace('+text', '')
                        print(f"Fixed mode from 'markers+lines+text' to '{trace.mode}' due to empty text")
                
                # Ensure marker is visible
                if hasattr(trace, 'marker'):
                    trace.marker.update(
                        size=10,  # Larger size for visibility
                        opacity=0.9,  # Higher opacity
                    )
                
                print(f"Adding trace with mode: {trace.mode}, color: {trace.line.color}")
                print(f"Trace data points: {len(trace.x)} x-coordinates, {len(trace.y)} y-coordinates")
                print(f"Line properties: {trace.line}")
                print(f"Marker properties: {trace.marker}")
                fig.add_trace(trace)
                color_idx += 1

            # Add a category
            elif value in label2node:
                print(f"\tAdd label:\t{value}")

                for idx_node, node in enumerate(label2node[value]):
                    trace = node2trace[node]
                    # Haven't tested this since I believe category is broken (after adding only a subset of node trajectories)
                    trace = convert_scatter_to_scattergl(trace)
                    trace.line['color'] = label2colors[value][idx_node % 12]
                    fig.add_trace(trace)

        # Debug: print final figure traces
        print(f"Final figure has {len(fig.data)} traces:")
        for i, trace in enumerate(fig.data):
            print(f"  Trace {i}: {trace.name} (type: {type(trace)}, mode: {trace.mode})")
            if hasattr(trace, 'x') and trace.x:
                print(f"    X range: {min(trace.x)} to {max(trace.x)}")
                print(f"    Y range: {min(trace.y)} to {max(trace.y)}")
        
        # Debug: print figure layout
        print(f"Figure layout: {fig.layout}")


    # elif action_name == 'update-color-button':
    #     # Update the color of the selected trajectory
    #     del figure_name2trace['background']
    #     figure_name2trace[selected_node].line['color'] = selected_color['hex']
    #
    #     add_traces()

    elif action_name == 'dygetviz':
        # Add annotations when user clicks on a node
        """
                Upon clicking a node, if the node's display is on, we turn the display off. If its display is off, we turn the display on.
                """

        if clickData:
            del figure_name2trace['background']
            point_data = clickData['points'][0]
            point_idx = point_data['pointIndex']

            displayed_text = np.array(
                list(node2trace['background']['text'])).astype(
                '<U50')

            displayed_text[point_idx] = node2trace['background']['hovertext'][
                point_idx] if not displayed_text[point_idx] else ''

            node2trace['background']['text'] = tuple(displayed_text.tolist())

            add_background()

            add_traces()

        #     point_name = df['name'].iloc[idx]
        #
        #     # Check if the point is already annotated
        #     existing_annotation = next((a for a in annotations if
        #                                 a['x'] == point_data['x'] and a['y'] ==
        #                                 point_data['y']), None)
        #
        #     if existing_annotation:
        #         # Remove existing annotation
        #         annotations.remove(existing_annotation)
        #     else:
        #         # Add new annotation
        #         annotations.append({
        #             'x': point_data['x'],
        #             'y': point_data['y'],
        #             'xref': 'x',
        #             'yref': 'y',
        #             'text': point_name,
        #             'showarrow': False
        #         })
        #
        # fig.update_layout(annotations=annotations)

    return fig, trajectory_names



# Upload callbacks disabled due to dash_mantine_components compatibility issues
# @app.callback(
#     Output("dataset-store", "data"),
#     Input("upload-data", "contents"),
#     State("upload-data", "filename"),
#     prevent_initial_call=True,
# )
# def store_data(contents, filename):
#     if contents is not None:
#         df = parse_contents(contents, filename)
#         return df.to_json(orient="split")
# 
# 
# @app.callback(
#     Output("output-data-upload", "children"),
#     Output("output-data-upload-preview", "children"),
#     Output("upload-data", "style"),
#     Output("upload-data", "children"),
#     Input("dataset-store", "data"),
# )
# def load_data(dataset):
#     if dataset is not None:
#         df = pd.read_json(dataset, orient="split")
#         table_preview = dag.AgGrid(
#             id="data-preview",
#             rowData=df.to_dict("records"),
#             style={"height": "275px"},
#             columnDefs=[{"field": i} for i in df.columns],
#         )
#         return (
#             table_preview,
#             table_preview,
#             {
#                 "borderWidth": "1px",
#                 "borderStyle": "dashed",
#                 "borderRadius": "5px",
#                 "textAlign": "center",
#                 "padding": "7px",
#                 "backgroundColor": "#fafafa",
#             },
#             dmc.Group(
#                 [
#                     html.Div(
#                         [
#                             "Drag and Drop or",
#                             dmc.Button(
#                                 "Replace file",
#                                 ml=10,
#                                 leftIcon=DashIconify(icon="mdi:file-replace"),
#                             ),
#                         ]
#                     )
#                 ],
#                 position="center",
#                 align="center",
#                 spacing="xs",
#             ),
#         )
#     return no_update


# @app.callback(
#     Output('node-selector', 'options'),
#     Input('trajectory-names-store', 'data')
# )
# def update_node_selector_options(trajectory_names):
#     """
#     Archived function
#     Adjust the colors of existing trajectories
#
#     :param trajectory_names:
#     """
#     if not trajectory_names:
#         return []  # return an empty list if trajectory_names is empty
#
#     # return a list of options for nodes in trajectory_names
#     return [{
#         'label': node,
#         'value': node
#     } for node in trajectory_names]


if __name__ == "__main__":
    print(const.DYGETVIZ)

    """
    `dev_tools_hot_reload`: disable hot-reloading. The code is not reloaded when the file is changed. Setting it to 
    `True` will make the code run very slow.
    """
    app.run(debug=True, dev_tools_hot_reload=True, use_reloader=True,
            port=args.port)

    # app.run_server(debug=True, port=args.port)


