"""Module with function to create containers for the app layout."""
from typing import List
from pathlib import Path
import numpy as np
import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc
from color_schemes import get_color_schemes, sample_color_scheme



def logo_title(app) -> html.Div:
    """Function to create the Div that containers the Pollination logo and app
    title (Design Explorer)."""
    container = html.Div(children=[
        html.Img(id='pollination-logo',
                 src=app.get_asset_url('pollination.svg'),
                 className='logo'),
        html.Span(children='Design Explorer (Local)',
                  className='app-name'),
        html.Div(children=[
            html.A('GitHub Repository', href='https://github.com/LoftyTao/design-explorer-local', 
                   target='_blank', className='github-link'),
            html.A('Tutorial', href='https://www.youtube.com/watch?v=X7hrUg71scE&t=28s', 
                   target='_blank', className='github-link'),
            html.A('教程视频', href='https://www.bilibili.com/video/BV16MxneEESV/?spm_id_from=333.1387.homepage.video_card.click&vd_source=75eb992bb7880d408ee082a7978f2d8a', 
                   target='_blank', className='github-link'),
        ], className='github-container'),
        html.Div(children=[
            html.Span('Based on: '),
            html.A('pollination-apps/design-explorer', href='https://github.com/pollination-apps/design-explorer', 
                   target='_blank', className='acknowledge-link'),
            html.Span(' and '),
            html.A('tt-acm/DesignExplorer', href='https://tt-acm.github.io/DesignExplorer/', 
                   target='_blank', className='acknowledge-link'),
        ], className='acknowledge-container')
    ],
        className='logo-title'
    )

    return container


def info_box():
    info_box = html.Div(
        [
            # Application description on separate line
            html.P(
                'Design Explorer - Visualize and explore design data with ease.',
                className='justify-text mb-4'
            ),
            
            # Two-column layout for features and usage
            dbc.Row([
                # First column: Key Features
                dbc.Col([
                    html.P(
                        'Key Features: '
                        '\n• Analyze and compare design configurations '
                        '\n• Color-code data points by parameters '
                        '\n• Explore images based on design variables '
                        '\n• Filter data with interactive parallel coordinates plot',
                        className='justify-text'
                    )
                ], md=6),
                # Second column: How to Use
                dbc.Col([
                    html.P(
                        'How to Use: '
                        '\n1. Select a sample project or upload your ZIP file '
                        '\n2. Use Color-by to highlight data points '
                        '\n3. Use Sort-by to organize images '
                        '\n4. Click images to view details '
                        '\n5. Use the parallel plot to filter results',
                        className='justify-text'
                    )
                ], md=6)
            ])
        ],
        className='info-box',
    )

    return info_box


def hello_user():
    """Function to create a Div for authentication of user (Offline)."""
    hello_user_container = html.Div(children=[
        html.Span(children='Offline Mode', className='hi-user'),
    ],
        id='hello',
        className='hello'
    )
    return hello_user_container



def create_radio_container() -> html.Div:
    """Function to create the radio items."""
    container = html.Div(
        children=[
            dbc.RadioItems(
                options=[
                    {'label': 'Sample Project', 'value': False},
                    {'label': 'Load from local ZIP file', 'value': True},
                ],
                value=False,
                id='radio-items-input',
                inline=True
            ),
        ],
        id='radio-items',
        className='radio-items'
    )
    return container


def select_pollination_project():
    """Function to create a Div for selecting a project on Pollination."""
    select_project_label = html.Label(
        children='Load from ZIP', className='color-by-label')
    
    select_project_container = html.Div(
        children=[
            select_project_label,
            dcc.Upload(
                id='upload-data-component',
                children=html.Span(
                    children='Select ZIP File',
                    style={
                        'color': 'white',
                        'fontSize': '0.9rem',
                        'fontWeight': '500',
                        'textAlign': 'center',
                        'display': 'block'
                    }
                ),
                # Allow multiple files to be uploaded
                multiple=False,
                style={
                    'width': '100%',
                    'height': 'auto',
                    'cursor': 'pointer',
                    'margin': '0',
                    'padding': '0.5rem 1rem',
                    'border': 'none',
                    'borderRadius': '0.375rem',
                    'outline': 'none',
                    'boxSizing': 'border-box',
                    'backgroundColor': '#3b82f6',
                    'transition': 'all 0.2s ease',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center'
                }
            ),
            html.Div(
                children=[
                    html.Small(
                        children=[
                            'Tip: Use ',
                            html.A('Pollination Fly', href='https://docs.pollination.solutions/user-manual/grasshopper-plugin/grasshopper-user-interface/3_parametric/fly', target='_blank'),
                            ' and ',
                            html.A('Fly_ID', href='https://docs.pollination.solutions/user-manual/grasshopper-plugin/grasshopper-user-interface/3_parametric/fly_id', target='_blank'),
                            ' components to create associated files that meet the program requirements, ',
                            'then package them into a ZIP file yourself.'
                        ],
                        className='upload-tip'
                    )
                ],
                className='upload-tip-container'
            ),
            dcc.Dropdown(
                id='select-uploaded-project-dropdown',
                options=[],
                placeholder='Select uploaded project',
                style={'display': 'none'} # Initially hidden
            ),
            html.Div(id='output-data-upload'),
        ],
        id='select-pollination-project',
        className='select-pollination-project')

    return select_project_container



def select_sample_project() -> html.Div:
    """Function to create the Div that contains the options for coloring the
    parallel coordinates by a column."""
    children = []
    children.append(
        dbc.DropdownMenuItem(
            'Daylight Factor',
            id={'select_sample_project': 'daylight-factor'}))
    children.append(dbc.DropdownMenuItem(
        'Box', id={'select_sample_project': 'box'}))
    children.append(
        dbc.DropdownMenuItem(
            'Box Without Images',
            id={'select_sample_project': 'box-without-img'}))
    dropdown_menu = dbc.DropdownMenu(
        id='select-sample-dropdown',
        label='Daylight Factor',
        children=children,
        direction='end',
        size='md'
    )

    select_sample_label = html.Label(
        children='Select sample', className='color-by-label')

    select_sample_container = html.Div(
        className='select-sample',
        id='select-sample',
        children=[select_sample_label, dropdown_menu]
    )

    return select_sample_container


def create_color_by_children(parameters, color_by) -> List[html.Div]:
    """Function to create the children for the options for coloring the
    parallel coordinates by a column."""
    children = []
    children_input = []
    children_output = []
    for value in parameters.values():
        label = value['label']
        if value['type'] == 'in':
            children_input.append(
                dbc.DropdownMenuItem(value['display_name'],
                                     id={'color_by_dropdown': f'{label}'})
            )
        if value['type'] == 'out':
            children_output.append(
                dbc.DropdownMenuItem(value['display_name'],
                                     id={'color_by_dropdown': f'{label}'})
            )
    children.append(dbc.DropdownMenuItem(
        'None', id={'color_by_dropdown': False}))
    children.append(dbc.DropdownMenuItem('Divider', divider=True))
    children.append(dbc.DropdownMenuItem('Output', header=True))
    children.extend(children_output)
    children.append(dbc.DropdownMenuItem('Divider', divider=True))
    children.append(dbc.DropdownMenuItem('Input', header=True))
    children.extend(children_input)
    dropdown_menu = dbc.DropdownMenu(
        id='color-by-dropdown',
        label=parameters[color_by]['display_name'],
        children=children,
        direction='end',
        size='md'
    )

    store = dcc.Store(id='color-by-column', data=color_by)
    color_by_label = html.Label(
        children='Color by', className='color-by-label')

    # Add color scheme selection
    color_scheme_label = html.Label(
        children='Color scheme', className='color-by-label')
    color_scheme_dropdown = dbc.DropdownMenu(
        id='color-scheme-dropdown',
        label='Original',
        children=[
            dbc.DropdownMenuItem('Original', id={'color_scheme': 'Original'}),
            dbc.DropdownMenuItem('Nuanced', id={'color_scheme': 'Nuanced'}),
            dbc.DropdownMenuItem('Multi-Colored', id={'color_scheme': 'Multi-Colored'}),
            dbc.DropdownMenuItem('Parula', id={'color_scheme': 'Parula'}),
        ],
        direction='end',
        size='md'
    )
    color_scheme_store = dcc.Store(id='color-scheme', data='Original')

    children = [color_by_label, dropdown_menu, color_scheme_label, color_scheme_dropdown, store, color_scheme_store]

    return children


def create_color_by_container(parameters, color_by) -> html.Div:
    """Function to create the Div that contains the options for coloring the
    parallel coordinates by a column."""
    children = create_color_by_children(parameters, color_by)

    color_by_container = html.Div(
        className='color-by',
        id='color-by',
        children=children
    )

    return color_by_container


def create_sort_by_children(parameters, sort_by) -> html.Div:
    """Function to create the Div that contains the options for sorting the
    images in the grid."""
    children = []
    children_input = []
    children_output = []
    for value in parameters.values():
        label = value['label']
        if value['type'] == 'in':
            children_input.append(
                dbc.DropdownMenuItem(value['display_name'],
                                     id={'sort_by_dropdown': f'{label}'})
            )
        if value['type'] == 'out':
            children_output.append(
                dbc.DropdownMenuItem(value['display_name'],
                                     id={'sort_by_dropdown': f'{label}'})
            )
    children.append(dbc.DropdownMenuItem('Output', header=True))
    children.extend(children_output)
    children.append(dbc.DropdownMenuItem('Divider', divider=True))
    children.append(dbc.DropdownMenuItem('Input', header=True))
    children.extend(children_input)
    dropdown_menu = dbc.DropdownMenu(
        id='sort-by-dropdown',
        label=parameters[sort_by]['display_name'],
        children=children,
        direction='end',
        size='md'
    )

    sort_by_store = dcc.Store(id='sort-by-column', data=sort_by)
    button_icon = html.I(id='button-ascending-icon',
                         className='bi bi-sort-down')
    button_ascending = dbc.Button(children=[button_icon],
                                  id='button-ascending',
                                  class_name='sort-by-button',
                                  size='sm')
    sort_ascending_store = dcc.Store(id='sort-ascending', data=False)
    sort_by_label = html.Label(children='Sort by',
                               id='sort-by-label',
                               className='sort-by-label')

    children = [sort_by_label, dropdown_menu, button_ascending, sort_by_store,
                sort_ascending_store]

    return children


def create_images_grid_children(
        sorted_df_records, color_by, minimum, maximum, img_column,
        project_folder, color_scheme='Original') -> List[html.Div]:
    children = []
    project_folder = Path(project_folder)
    color_schemes = get_color_schemes()
    current_scheme = color_schemes.get(color_scheme, color_schemes['Original'])
    
    for record in sorted_df_records:
        # Get the border color based on the selected color scheme
        border_color = sample_color_scheme(current_scheme, record[color_by], minimum, maximum)
        src = project_folder.joinpath(record[img_column])
        image = html.Div(
            html.Img(src=src.as_posix(),
                     id={'image': f'{record[img_column]}'},
                     className='image-grid',
                     style={'borderColor': border_color}
                     ),
            style={
                'aspectRatio': '1',
                'width': '100%',
                'height': '100%',
                'position': 'relative',
                'display': 'flex',
                'alignItems': 'center',
                'justifyContent': 'center',
            }
        )
        children.append(image)

    return children


def create_images_container(images_div, parameters, sort_by) -> html.Div:
    """Function to create a Div for images."""
    children = create_sort_by_children(parameters, sort_by)
    sort_container = html.Div(
        children=children,
        className='sort-by',
        id='sort-by'
    )

    images_container = html.Div(
        [dcc.Store(id='selected-image-data'),
         html.Div(
             [html.Div(
                 id='selected-image-info', className='selected-image-info'),
              html.Div(
                  children=[html.Img(
                      id='selected-image',
                      className='selected-image')],
                  id='selected-image-wrapper',
                  className='selected-image-wrapper')],
             id='selected-image-container',
             className='selected-image-container'),
         html.Div(
             children=images_div, id='images-grid', className='images-grid')],
        id='images-container', className='images-container')

    main_images_container = html.Div([
        sort_container, images_container
    ],
        id='main-images-container', className='main-images-container'
    )

    return main_images_container


def create_sort_by_container(parameters, sort_by) -> html.Div:
    """Function to create the Div that contains the options for sorting the
    images by a column."""
    children = create_sort_by_children(parameters, sort_by)
    sort_container = html.Div(
        children=children,
        className='sort-by',
        id='sort-by'
    )

    return sort_container

