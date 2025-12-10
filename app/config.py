"""Config."""
import os
from pathlib import Path

assets_path = Path(__file__).parent.joinpath('assets')
static_path = Path(__file__).parent.joinpath('static')
upload_path = static_path.joinpath('uploaded')
pollination_path = Path(__file__).parent.joinpath('pollination')
base_path = os.getenv('POLLINATION_API_URL', 'https://api.staging.pollination.solutions')
