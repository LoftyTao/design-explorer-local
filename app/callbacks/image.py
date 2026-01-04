"""Module for image callbacks."""
from pathlib import Path
import dash
from dash import html, ALL, ctx
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import numpy as np
import dash_bootstrap_components as dbc

from color_schemes import get_color_schemes, sample_color_scheme


@dash.callback(
    Output('images-grid', 'children', allow_duplicate=True),
    [Input('active-records', 'data'),
     State('df', 'data'),
     Input('color-by-column', 'data'),
     Input('sort-by-column', 'data'),
     Input('sort-ascending', 'data'),
     Input('color-scheme', 'data'),
     Input('selected-image-group', 'data'),
     State('project-folder', 'data'),
     State('selected-image-data', 'data')],
    prevent_initial_call=True,
)
def update_images_grid(
        active_records, df_records, color_by_column, sort_by_column,
        sort_ascending, color_scheme, img_column, project_folder, selected_image_data):
    """Update the images grid based on the selected image group."""
    if img_column is None:
        return []
    
    images_div = []
    minimum = None
    maximum = None
    
    if color_by_column:
        dff = pd.DataFrame.from_records(df_records)
        minimum, maximum = dff[color_by_column].min(), dff[color_by_column].max()
    
    border_color = '#636EFA'
    
    # Get selected image filename if any
    selected_image = None
    if selected_image_data and isinstance(selected_image_data, list) and len(selected_image_data) > 0:
        selected_image = selected_image_data[0].get(img_column)
    
    # Handle both string and Path objects for project_folder
    if isinstance(project_folder, str):
        project_folder_path = project_folder
    else:
        project_folder_path = project_folder
    
    color_schemes = get_color_schemes()
    current_scheme = color_schemes.get(color_scheme, color_schemes['Original'])
    
    for d in active_records:
        if color_by_column:
            # Use the selected color scheme to get border color
            border_color = sample_color_scheme(current_scheme, d[color_by_column], minimum, maximum)
        
        if isinstance(project_folder_path, str):
            src = f"{project_folder_path}/{d[img_column]}"
        else:
            src = project_folder_path.joinpath(d[img_column]).as_posix()
        
        # Check if this image is selected
        is_selected = selected_image == d[img_column]
        image_class = 'image-grid selected' if is_selected else 'image-grid'
        
        image = html.Div(
            html.Img(src=src,
                     id={'image': f'{d[img_column]}'},
                     className=image_class,
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
        images_div.append(image)

    return images_div


@dash.callback(
    [Output('selected-image-data', 'data', allow_duplicate=True),
     Output('selected-image-info', 'children', allow_duplicate=True)],
    [Input({'image': ALL}, 'n_clicks'),
     State('df', 'data'),
     State('labels', 'data'),
     State('selected-image-group', 'data'),
     State('parameters', 'data')],
    prevent_initial_call=True
)
def update_clicked_image_grid(
        n_clicks, df_records, labels, current_group, parameters):
    """If a click is registered in any of the images in images-grid, data is
    updated in selected-image-table. The image group is preserved."""
    if all(item is None for item in n_clicks):
        # no clicks, no update
        return (dash.no_update,) * 2
    # get the clicked image
    image_id = ctx.triggered_id.image
    dff = pd.DataFrame.from_records(df_records)
    
    # Find the selected image's row using the current image group
    if current_group and current_group in dff.columns:
        selected_df = dff.loc[dff[current_group] == image_id]
    else:
        # Fallback: find any matching image column
        for col in dff.columns:
            if col.startswith('img:'):
                selected_df = dff.loc[dff[col] == image_id]
                if not selected_df.empty:
                    break
        else:
            return (dash.no_update,) * 2
    
    if selected_df.empty:
        return (dash.no_update,) * 2
    
    select_image_info = []
    record = selected_df.to_dict('records')
    for label in labels:
        select_image_info.append(
            html.Div(
                children=[html.Span(
                    f'{parameters[label]["display_name"]}: ',
                    className='label-bold'),
                    f'{record[0][label]}']))
    return record, select_image_info


@dash.callback(
    Output('image-group-display', 'children'),
    [Input('selected-image-data', 'data'),
     Input('selected-image-group', 'data'),
     State('image-columns', 'data')],
    prevent_initial_call=True
)
def update_image_group_display(selected_image_data, current_group, image_columns):
    """Display the current image group name when an image is selected."""
    if not selected_image_data or not image_columns or len(image_columns) <= 1:
        return None
    
    # Show current group name
    group_name = current_group.split(':')[1] if current_group else 'Unknown'
    
    return html.Div([
        html.Span('Viewing: ', className='me-1'),
        dbc.Badge(
            group_name,
            color='primary',
            className='image-group-badge'
        )
    ], className='image-group-display-container')


@dash.callback(
    Output('image-navigation-buttons', 'children'),
    [Input('selected-image-data', 'data'),
     State('image-columns', 'data')],
    prevent_initial_call=True
)
def update_navigation_buttons(selected_image_data, image_columns):
    """Update navigation buttons when an image is selected."""
    if not selected_image_data or not image_columns or len(image_columns) <= 1:
        return None
    
    buttons = html.Div([
        dbc.Button(
            '◀ Previous',
            id='btn-prev-image-group',
            color='primary',
            size='sm',
            className='me-2'
        ),
        dbc.Button(
            'Next ▶',
            id='btn-next-image-group',
            color='primary',
            size='sm'
        )
    ], className='d-flex justify-content-center mt-3')
    
    return buttons


@dash.callback(
    Output('selected-image', 'src', allow_duplicate=True),
    Output('selected-image-info', 'children', allow_duplicate=True),
    Output('selected-image-group', 'data', allow_duplicate=True),
    [Input('btn-prev-image-group', 'n_clicks'),
     Input('btn-next-image-group', 'n_clicks')],
    [State('selected-image-data', 'data'),
     State('image-columns', 'data'),
     State('selected-image-group', 'data'),
     State('df', 'data'),
     State('project-folder', 'data'),
     State('labels', 'data'),
     State('parameters', 'data')],
    prevent_initial_call=True
)
def navigate_image_groups(prev_clicks, next_clicks, selected_image_data, 
                          image_columns, current_group, df_records, project_folder, 
                          labels, parameters):
    """Navigate to previous or next image group for the same variables."""
    if not selected_image_data or not image_columns or len(image_columns) <= 1:
        return dash.no_update, dash.no_update, dash.no_update
    
    triggered_id = ctx.triggered_id
    if not triggered_id:
        return dash.no_update, dash.no_update, dash.no_update
    
    # Find current index
    current_index = image_columns.index(current_group)
    
    # Calculate new index
    if triggered_id == 'btn-prev-image-group':
        new_index = (current_index - 1) % len(image_columns)
    elif triggered_id == 'btn-next-image-group':
        new_index = (current_index + 1) % len(image_columns)
    else:
        return dash.no_update, dash.no_update, dash.no_update
    
    # Get the new image group
    new_group = image_columns[new_index]
    
    # Get the current record (same variables, different image)
    current_record = selected_image_data[0]
    
    # Find the corresponding image in the new group by comparing non-image columns
    dff = pd.DataFrame.from_records(df_records)
    
    # Build filter criteria from non-image columns
    filter_criteria = {}
    for col in dff.columns:
        if not col.startswith('img:'):
            value = current_record.get(col)
            if value is not None:
                filter_criteria[col] = value
    
    # Find matching record(s)
    matching_indices = []
    for idx, row in dff.iterrows():
        match = True
        for col, val in filter_criteria.items():
            if row[col] != val:
                match = False
                break
        if match:
            matching_indices.append(idx)
    
    if matching_indices and new_group in dff.columns:
        # Get the first matching record
        new_record = dff.loc[matching_indices[0]].to_dict()
        new_img = new_record.get(new_group)
        
        if new_img:
            # Build image source
            if isinstance(project_folder, str):
                src = f"{project_folder}/{new_img}"
            else:
                src = Path(project_folder).joinpath(new_img).as_posix()
            
            # Update image info
            select_image_info = []
            for label in labels:
                select_image_info.append(
                    html.Div(
                        children=[html.Span(
                            f'{parameters[label]["display_name"]}: ',
                            className='label-bold'),
                            f'{new_record[label]}']))
            
            return src, select_image_info, new_group
    
    return dash.no_update, dash.no_update, dash.no_update


@dash.callback(
    Output('images-container', 'style', allow_duplicate=True),
    Input('img-column', 'data'),
    prevent_initial_call=True
)
def update_images_grid_div_display(img_column):
    """If img-column is None, display is changed to none."""
    if img_column is None:
        return {'display': 'none'}
    else:
        return {}


@dash.callback(
    Output('selected-image', 'src', allow_duplicate=True),
    Output('selected-image-container', 'style', allow_duplicate=True),
    Output('images-grid', 'style', allow_duplicate=True),
    [Input('selected-image-data', 'data')],
    [State('selected-image-group', 'data'),
     State('project-folder', 'data')],
    prevent_initial_call=True
)
def update_selected_image_table(
        selected_image_data, img_column, project_folder):
    """If the data in selected-image-table is changed.
    
    The src of selected-image is taken from selected-image-table. The styles of
    selected-image-container and images-grid are also updated."""
    if selected_image_data is None or img_column is None:
        return (dash.no_update,) * 3

    # Handle both string and Path objects for project_folder
    if isinstance(project_folder, str):
        src = f"{project_folder}/{selected_image_data[0][img_column]}"
    else:
        project_folder_path = Path(project_folder)
        src = project_folder_path.joinpath(
            selected_image_data[0][img_column]).as_posix()

    selected_image_container_style = {
        'width': '75%'
    }

    images_grid_style = {
        'grid-template-columns': 'repeat(auto-fill, minmax(10%, 1fr))',
        'width': '25%'
    }

    return src, selected_image_container_style, images_grid_style


@dash.callback(
    [Output('selected-image', 'src', allow_duplicate=True),
     Output('selected-image', 'n_clicks', allow_duplicate=True),
     Output('selected-image-data', 'data', allow_duplicate=True),
     Output('selected-image-info', 'children', allow_duplicate=True),
     Output('selected-image-container', 'style', allow_duplicate=True),
     Output('images-grid', 'style', allow_duplicate=True)],
    Input('selected-image', 'n_clicks'),
    prevent_initial_call=True
)
def update_click_selected_image(n_clicks):
    """If a click is registered on selected-image.
    
    When this happens we reset everything related to the selected-image. The
    style of images-grid is also reset to its original state."""
    if n_clicks is not None:
        selected_image_container_style = {}
        images_grid_style = {}
        return None, None, None, None, selected_image_container_style, images_grid_style
