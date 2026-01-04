"""Config."""
import os
from pathlib import Path

assets_path = Path(__file__).parent.joinpath('assets')
static_path = Path(__file__).parent.joinpath('static')
upload_path = static_path.joinpath('uploaded')
pollination_path = Path(__file__).parent.joinpath('pollination')
base_path = os.getenv('POLLINATION_API_URL', 'https://api.staging.pollination.solutions')
samples_path = assets_path.joinpath('samples')


def get_sample_projects():
    """Dynamically scan the samples directory and return a dictionary of sample projects."""
    sample_projects = {}
    if not samples_path.exists():
        return sample_projects
    
    for item in samples_path.iterdir():
        if item.is_dir():
            folder_name = item.name
            data_csv = item.joinpath('data.csv')
            if data_csv.exists():
                display_name = folder_name.replace('-', ' ').replace('_', ' ').title()
                sample_projects[folder_name] = {
                    'id': folder_name,
                    'display_name': display_name
                }
    
    return sample_projects
