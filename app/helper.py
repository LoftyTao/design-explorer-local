"""Module with helper functions."""
import pandas as pd
import socket


def process_dataframe(df: pd.DataFrame):
    labels = {}
    parameters = {}
    input_columns = []
    output_columns = []
    image_columns = []
    for col_name, col_series in df.items():
        col_type, col_id = col_name.split(':')
        if col_type != 'img':
            labels[col_name] = col_id
            parameters[col_name] = {
                'label': col_name, 
                'display_name': col_id,
                'type': col_type
            }
            if col_type == 'in':
                input_columns.append(col_name)
            elif col_type == 'out':
                output_columns.append(col_name)
        else:
            image_columns.append(col_name)

    return labels, parameters, input_columns, output_columns, image_columns


def find_free_port(start_port=8050, max_tries=50):
    """
    Try to find an available TCP port starting from start_port.
    Returns the available port number.
    """
    port = start_port
    for _ in range(max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                port += 1
    raise RuntimeError("Could not find a free port.")

ASCII_ART = r"""
  _____            _               ______            _                     
 |  __ \          (_)             |  ____|          | |                    
 | |  | | ___  ___ _  __ _ _ __   | |__  __  ___ __ | | ___  _ __ ___ _ __ 
 | |  | |/ _ \/ __| |/ _` | '_ \  |  __| \ \/ / '_ \| |/ _ \| '__/ _ \ '__|
 | |__| |  __/\__ \ | (_| | | | | | |____ >  <| |_) | | (_) | | |  __/ |   
 |_____/ \___||___/_|\__, |_| |_| |______/_/\_\ .__/|_|\___/|_|  \___|_|   
                      __/ |                   | |                          
                     |___/                    |_|                          
"""

def print_startup_banner(port: int=8050, app_name: str="Design Explorer"):
    """
    Print startup information to console when launching the application.
    """
    print(ASCII_ART)
    print(f"{app_name}")
    print("============================================")
    print("Open this link in your browser:")
    print(f"  -> http://127.0.0.1:{port}/")
    print("")
    print("How to stop:")
    print("  - Close this window, or")
    print("  - Press Ctrl+C in this console.")
    print("============================================")
    print("")