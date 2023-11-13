"""Test MantineProvider fix for dash_mantine_components."""

import dash
from dash import html
import dash_mantine_components as dmc

# Create a simple app to test MantineProvider
app = dash.Dash(__name__)

# Simple layout with MantineProvider
app.layout = dmc.MantineProvider(
    html.Div([
        html.H1("Test MantineProvider"),
        dmc.Container([
            dmc.Stack([
                dmc.Button("Test Button", color="blue"),
                html.P("If you see this without errors, MantineProvider is working!")
            ])
        ])
    ])
)

if __name__ == '__main__':
    print("Testing MantineProvider...")
    print("Visit http://127.0.0.1:8055/ to test")
    app.run(debug=True, port=8055)