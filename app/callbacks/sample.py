"""Module for sample callbacks."""
import dash
from dash import ALL, ctx
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

from containers import create_color_by_children, create_sort_by_children
from helper import process_dataframe
from samples import sample_alias
from config import assets_path, samples_path


@dash.callback(
    [Output('project-folder', 'data', allow_duplicate=True),
     Output('df', 'data', allow_duplicate=True),
     Output('active-records', 'data', allow_duplicate=True),
     Output('active-filters', 'data', allow_duplicate=True),
     Output('df-columns', 'data', allow_duplicate=True),
     Output('labels', 'data', allow_duplicate=True),
     Output('img-column', 'data', allow_duplicate=True),
     Output('image-columns', 'data', allow_duplicate=True),
     Output('parameters', 'data', allow_duplicate=True),
     Output('parallel-coordinates', 'figure', allow_duplicate=True),
     Output('select-sample-dropdown', 'label', allow_duplicate=True),
     Output('sort-by', 'children', allow_duplicate=True),
     Output('color-by', 'children', allow_duplicate=True),
     Output('table', 'columns', allow_duplicate=True),
     Output('selected-image-info', 'children', allow_duplicate=True),
     Output('selected-image-container', 'style', allow_duplicate=True),
     Output('main-images-container', 'style', allow_duplicate=True),
     Output('images-grid', 'style', allow_duplicate=True),
     Output('selected-image-group', 'data', allow_duplicate=True),
     Output('image-navigation-buttons', 'children', allow_duplicate=True)],
    Input({'select_sample_project': ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def update_sample_project(n_clicks):
    """If a click is registered in sort by dropdown, data is updated in
    sort-by-column, and label is updated in sort-by-dropdown."""
    sample_project = ctx.triggered_id.select_sample_project
    project_folder = f'assets/samples/{sample_project}'
    select_sample_dropdown_label = sample_alias[sample_project]['display_name']
    csv = samples_path.joinpath(sample_project, 'data.csv')
    dff = pd.read_csv(csv)
    df_records = dff.to_dict('records')

    labels, parameters, input_columns, output_columns, image_columns = \
        process_dataframe(dff)

    # color by first output column, or first input column
    if output_columns:
        color_by = output_columns[0]
        sort_by = output_columns[0]
    else:
        color_by = input_columns[0]
        sort_by = output_columns[0]

    fig = px.parallel_coordinates(dff, color=color_by, labels=labels)

    img_columns = dff.filter(regex=f'^img:').columns
    if img_columns.empty:
        img_column = None
        img_columns_list = []
    else:
        img_column = img_columns[0]
        img_columns_list = img_columns.tolist()

    columns = []
    for value in parameters.values():
        if value['type'] != 'img':
            columns.append(
                {'id': value['label'],
                 'name': value['display_name']})
        else:
            columns.append(
                {'id': value['label'],
                 'name': value['display_name'],
                 'hidden': True})

    sort_by_children = create_sort_by_children(parameters, sort_by)
    color_by_children = create_color_by_children(parameters, color_by)

    active_filters = {}
    selected_image_info = None
    selected_image_container_style = {}
    main_images_container_style = {}
    images_grid_style = {}

    if not img_column:
        main_images_container_style = {'display': 'none'}

    # Set image group dropdown label and selected group
    if img_columns_list:
        selected_image_group = img_columns_list[0]
        image_navigation_buttons = None
    else:
        selected_image_group = None
        image_navigation_buttons = None

    return (project_folder, df_records, df_records, active_filters, dff.columns,
            labels, img_column, img_columns_list, parameters, fig, select_sample_dropdown_label,
            sort_by_children, color_by_children, columns, selected_image_info,
            selected_image_container_style, main_images_container_style,
            images_grid_style, selected_image_group, image_navigation_buttons)