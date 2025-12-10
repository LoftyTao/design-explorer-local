"""Module for upload callbacks."""
import base64
import zipfile
import shutil
from io import BytesIO
from pathlib import Path
import dash
from dash import ctx
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px

from containers import create_color_by_children, create_sort_by_children
from helper import process_dataframe
from config import assets_path, upload_path, static_path


@dash.callback(
    [Output('select-sample', 'style'),
     Output('select-pollination-project', 'style')],
    [Input('radio-items-input', 'value')]
)
def toggle_input_method(load_from_zip):
    """Toggle between sample project selection and ZIP upload."""
    if load_from_zip:
        # Load from local ZIP file is selected
        return {'display': 'none'}, {'display': 'block'}
    else:
        # Sample Project is selected
        return {'display': 'block'}, {'display': 'none'}


@dash.callback(
    [Output('uploaded-projects-store', 'data'),
     Output('select-uploaded-project-dropdown', 'options'),
     Output('select-uploaded-project-dropdown', 'value'),
     Output('select-uploaded-project-dropdown', 'style')],
    [Input('upload-data-component', 'contents')],
    [State('upload-data-component', 'filename'),
     State('uploaded-projects-store', 'data')],
    prevent_initial_call=True
)
def process_upload(contents, filename, existing_projects):
    """Process uploaded ZIP file and update project list."""
    if contents is None:
        raise PreventUpdate

    existing_projects = existing_projects or []

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    # Use static/uploaded folder to store extracted files
    # ensure upload_path exists
    upload_path.mkdir(parents=True, exist_ok=True)
    
    file_path = Path(filename)
    # Use stem as unique identifier/folder name
    project_id = file_path.stem
    extract_dir = upload_path.joinpath(project_id)
    
    # Clean up existing directory if it exists
    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    extract_dir.mkdir(exist_ok=True)

    try:
        with zipfile.ZipFile(BytesIO(decoded)) as zf:
            zf.extractall(extract_dir)
            
        # Check for data.csv
        csv_file = extract_dir.joinpath('data.csv')
        if not csv_file.exists():
            # Try to find data.csv in subdirectories
            csv_files = list(extract_dir.rglob('data.csv'))
            if csv_files:
                csv_file = csv_files[0]
                # If found in subdirectory, we might want to move files or update path logic
                # For simplicity, we'll keep the extract_dir as the base for this project
                # but we need to know where the images are relative to it.
                # Let's assume images are relative to data.csv's parent.
            else:
                # TODO: Handle error - no data.csv found
                raise PreventUpdate

        # Add to existing projects if not present
        if project_id not in [p['value'] for p in existing_projects]:
            existing_projects.append({'label': project_id, 'value': project_id})
        
        # Update options
        options = existing_projects
        
        # Show dropdown
        style = {'display': 'block', 'width': '100%'}

        return existing_projects, options, project_id, style

    except Exception as e:
        print(f"Error processing upload: {e}")
        raise PreventUpdate


@dash.callback(
    [Output('project-folder', 'data', allow_duplicate=True),
     Output('df', 'data', allow_duplicate=True),
     Output('active-records', 'data', allow_duplicate=True),
     Output('active-filters', 'data', allow_duplicate=True),
     Output('df-columns', 'data', allow_duplicate=True),
     Output('labels', 'data', allow_duplicate=True),
     Output('img-column', 'data', allow_duplicate=True),
     Output('parameters', 'data', allow_duplicate=True),
     Output('parallel-coordinates', 'figure', allow_duplicate=True),
     Output('sort-by', 'children', allow_duplicate=True),
     Output('color-by', 'children', allow_duplicate=True),
     Output('table', 'columns', allow_duplicate=True),
     Output('selected-image-info', 'children', allow_duplicate=True),
     Output('selected-image-container', 'style', allow_duplicate=True),
     Output('main-images-container', 'style', allow_duplicate=True),
     Output('images-grid', 'style', allow_duplicate=True)],
    [Input('select-uploaded-project-dropdown', 'value')],
    prevent_initial_call=True
)
def load_uploaded_project_data(project_id):
    """Load data when an uploaded project is selected."""
    if not project_id:
        raise PreventUpdate

    # Construct path based on project_id
    project_dir = upload_path.joinpath(project_id)
    
    # Find data.csv again (could optimize by storing path in store)
    csv_file = project_dir.joinpath('data.csv')
    if not csv_file.exists():
        csv_files = list(project_dir.rglob('data.csv'))
        if csv_files:
            csv_file = csv_files[0]
        else:
            raise PreventUpdate
            
    # Set project folder for serving static files
    # The app serves /static/uploaded at static/uploaded
    # We need the path relative to static/uploaded for the URL construction if we used a simple static route
    # But here we likely need the full path that the frontend can use.
    # If app.py serves '/static/uploaded' -> 'app/static/uploaded'
    # Then project_folder should be 'static/uploaded/{project_id}' (+ subdirs if any)
    
    # Let's find relative path from upload_path to csv_file's directory
    # This handles the case where data.csv is inside a subfolder in the zip
    rel_path = csv_file.parent.relative_to(upload_path)
    project_folder = f'uploaded/{rel_path.as_posix()}'

    dff = pd.read_csv(csv_file)
    df_records = dff.to_dict('records')

    labels, parameters, input_columns, output_columns, image_columns = \
        process_dataframe(dff)

    # color by first output column, or first input column
    if output_columns:
        color_by = output_columns[0]
        sort_by = output_columns[0]
    else:
        color_by = input_columns[0]
        sort_by = input_columns[0]

    fig = px.parallel_coordinates(dff, color=color_by, labels=labels)

    img_columns = dff.filter(regex=f'^img:').columns
    if img_columns.empty:
        img_column = None
    else:
        img_column = img_columns[0]

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
    selected_image_container_style = {}
    if not img_column:
        main_images_container_style = {'display': 'none'} # Or hidden

    return (project_folder, df_records, df_records, active_filters, list(dff.columns),
            labels, img_column, parameters, fig,
            sort_by_children, color_by_children, columns, selected_image_info,
            selected_image_container_style, main_images_container_style,
            images_grid_style)




