"""Module for app."""
from pathlib import Path
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from flask import send_from_directory

from containers import logo_title, info_box, hello_user, create_radio_container, \
    select_pollination_project, select_sample_project, create_color_by_container, \
    create_images_container
from config import assets_path, upload_path, static_path
from samples import load_sample_project

# import callback functions
from callbacks import color, image, records, sample, sort, table, upload

#
from waitress import serve
from helper import find_free_port, print_startup_banner


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.MATERIA, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True
)
app.title = 'Design Explorer'
server = app.server

# this will set an alternative folder for images (alternative to "/assets")
@server.route('/pollination/<path:path>')
def serve_image(path):
    directory = Path(__file__).parent.joinpath('pollination')
    return send_from_directory(directory, path)


# Serve uploaded files directly from static/uploaded to avoid Dash caching and reload issues
@server.route('/uploaded/<path:path>')
def serve_uploaded(path):
    return send_from_directory(upload_path, path)


parameters, color_by, fig, images_grid_children, sort_by, project_folder, \
df_records, df, labels, img_column, columns = load_sample_project(
    'daylight-factor'
)

app.layout = dbc.Container([
    # Header section
    logo_title(app),
    
    # Info section
    dbc.Row([
        dbc.Col(info_box(), md=12),
    ], className='mb-4'),
    
    # Project selection section
    dbc.Card([
        dbc.CardBody([
            create_radio_container(),
            html.Div([
                select_sample_project(),
                select_pollination_project(),
            ], className='mt-3'),
        ])
    ], className='mb-4 shadow-sm'),
    
    # Color by section
    create_color_by_container(parameters, color_by),
    
    # Parallel coordinates graph
    dbc.Card([
        dbc.CardBody([
            dcc.Graph(id='parallel-coordinates', figure=fig),
        ])
    ], className='mb-4 shadow-sm'),
    
    # Images container
    create_images_container(images_grid_children, parameters, sort_by),
    
    # Data table section
    dbc.Card([
        dbc.CardBody([
            dash_table.DataTable(
                id='table', 
                data=df.to_dict('records'),
                columns=columns,
                style_table={
                    'padding': '20px',
                    'overflowX': 'auto',
                    'overflowY': 'auto',
                    'maxHeight': '400px'
                },
                sort_action='native',
                fixed_rows={'headers': True},
                style_cell={'textAlign': 'left', 'padding': '8px', 'minWidth': '100px', 'width': '150px', 'maxWidth': '200px'},
                style_header={'backgroundColor': '#f8fafc', 'fontWeight': 'bold', 'borderBottom': '2px solid #e2e8f0'},
                style_data_conditional=[
                    {'if': {'row_index': 'odd'}, 'backgroundColor': '#f8fafc'}
                ]
            ),
        ])
    ], className='mb-4 shadow-sm'),
    
    # Hidden stores
    dcc.Store(id='project-folder', data=project_folder),
    dcc.Loading(children=[dcc.Store(id='df', data=df_records)],
        className='custom-spinner', type='default', fullscreen=True),
    dcc.Store(id='df-columns', data=df.columns),
    dcc.Store(id='labels', data=labels),
    dcc.Store(id='parameters', data=parameters),
    dcc.Store(id='img-column', data=img_column),
    dcc.Store(id='active-filters', data={}),
    dcc.Store(id='active-records', data=df_records),
    dcc.Store(id='uploaded-projects-store', data=[]),
    dcc.Store(id='parallel-coordinates-figure-highlight', data={}),
    dcc.Store(id='parallel-coordinates-figure', data=fig),
], style={'padding': '20px'}, fluid=True)


if __name__ == '__main__':
    # Find an available port
    port = find_free_port(8050)
    print_startup_banner(port=port)
    # Run app, use WSGI production server instead of Flask
    serve(app, host="127.0.0.1", port=port)






