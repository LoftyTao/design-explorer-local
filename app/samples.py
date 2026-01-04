"""Module for samples."""
from pathlib import Path
import pandas as pd
import plotly.express as px

from containers import create_images_grid_children
from helper import process_dataframe
from config import get_sample_projects


sample_alias = get_sample_projects()


def load_sample_project(sample_identifier: str = None):
    from config import samples_path
    
    if sample_identifier is None:
        sample_identifier = list(sample_alias.keys())[0]
    
    project_folder = f'assets/samples/{sample_identifier}'
    csv = samples_path.joinpath(sample_identifier, 'data.csv')
    df = pd.read_csv(csv)
    df_records = df.to_dict('records')

    labels, parameters, input_columns, output_columns, image_columns = \
        process_dataframe(df)

    # color by first output column, or first input column
    if output_columns:
        color_by = output_columns[0]
        sort_by = output_columns[0]
    else:
        color_by = input_columns[0]
        sort_by = output_columns[0]

    fig = px.parallel_coordinates(df, color=color_by, labels=labels)

    img_column = df.filter(regex=f'^img:').columns[0]
    image_columns = df.filter(regex=f'^img:').columns.tolist()

    minimum, maximum = df[color_by].min(), df[color_by].max()
    sorted_df = df.sort_values(by=sort_by, ascending=False)
    sorted_df_records = sorted_df.to_dict('records')
    images_grid_children = create_images_grid_children(
        sorted_df_records, color_by, minimum, maximum, img_column, project_folder, 'Original')

    columns = []
    for value in parameters.values():
        if value['type'] != 'img':
            columns.append({'id': value['label'], 'name': value['display_name']})
        else:
            columns.append(
                {'id': value['label'], 'name': value['display_name'], 'hidden': True})

    return (parameters, color_by, fig, images_grid_children, sort_by, project_folder,
            df_records, df, labels, img_column, columns, image_columns)
