"""Module for color callbacks."""
import dash
from dash import Patch, ALL, ctx
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import numpy as np

from color_schemes import get_color_schemes, rgb_to_hex


@dash.callback(
    [Output('parallel-coordinates', 'figure', allow_duplicate=True),
     Output('color-by-column', 'data'),
     Output('color-by-dropdown', 'label')],
    [Input({'color_by_dropdown': ALL}, 'n_clicks'),
     State('df', 'data'),
     State('labels', 'data'),
     State('parallel-coordinates', 'figure')],
    prevent_initial_call=True
)
def update_color_by(n_clicks, df_records, labels, figure):
    """If a click is registered in the color by dropdown, the figure is updated
    in parallel-coordinates, the data is updated in color-by-column, and the
    label is updated in color-by-dropdown."""
    if all(v is None for v in n_clicks):
        return (dash.no_update,) * 3

    dff = pd.DataFrame.from_records(df_records)
    color_by = ctx.triggered_id.color_by_dropdown

    if color_by:
        new_fig = Patch()
        new_fig['data'][0]['dimensions'] = figure['data'][0]['dimensions']
        new_fig['data'][0]['line']['color'] = dff[color_by]
        return new_fig, color_by, labels[color_by]
    else:
        new_fig = Patch()
        new_fig['data'][0]['dimensions'] = figure['data'][0]['dimensions']
        new_fig['data'][0]['line']['color'] = None
        return new_fig, color_by, 'None'


@dash.callback(
    [Output('color-scheme', 'data'),
     Output('color-scheme-dropdown', 'label'),
     Output('parallel-coordinates', 'figure')],
    [Input({'color_scheme': ALL}, 'n_clicks')],
    [State('df', 'data'),
     State('color-by-column', 'data'),
     State('labels', 'data'),
     State('parallel-coordinates', 'figure')],
    prevent_initial_call=True
)
def update_color_scheme(n_clicks, df_records, color_by_column, labels, figure):
    """If a click is registered in the color scheme dropdown, update the color scheme.
    This will affect both the parallel coordinates plot and the image grid borders."""
    if all(v is None for v in n_clicks):
        return (dash.no_update,) * 3

    # Get the selected color scheme
    color_scheme = ctx.triggered_id.color_scheme
    
    # Update the parallel coordinates plot with the new color scale
    if color_by_column and df_records and figure:
        dff = pd.DataFrame.from_records(df_records)
        
        # Create a custom color scale from the selected scheme
        color_schemes = get_color_schemes()
        scheme = color_schemes[color_scheme]
        hex_colors = [rgb_to_hex(rgb) for rgb in scheme['colors']]
        
        # Create a new figure from scratch with the updated color scheme
        # This ensures all Plotly internals are properly updated for WebGL
        import plotly.express as px
        
        # Create a new parallel coordinates figure with the selected color scheme
        new_fig = px.parallel_coordinates(
            dff, 
            color=color_by_column, 
            labels=labels,
            color_continuous_scale=hex_colors
        )
        
        # Copy any custom layout properties from the original figure
        if 'layout' in figure:
            for key, value in figure['layout'].items():
                if key not in new_fig.layout:
                    new_fig.layout[key] = value
        
        return color_scheme, color_scheme, new_fig
    else:
        return color_scheme, color_scheme, dash.no_update
