# Design Explorer

A powerful tool for visualizing and exploring design data, built with Python and Dash.

## Features

- **Interactive Data Visualization**: Explore design data through parallel coordinates plots
- **Color-Coded Data Points**: Color data points by different parameters to identify patterns
- **Image Exploration**: View and compare images based on design parameters
- **Sorting and Filtering**: Sort images by any parameter and filter data with the parallel coordinates plot
- **Sample Projects**: Built-in sample projects for quick exploration
- **ZIP File Upload**: Load custom design data from ZIP files
- **Responsive Design**: Works well on different screen sizes

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Dependencies

1. Clone the repository:

```bash
git clone https://github.com/yourusername/design-explorer.git
cd design-explorer
```

2. Create a virtual environment (optional but recommended):

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Run the Application

```bash
cd app
python app.py
```

The application will start on http://127.0.0.1:8050/

### Using Design Explorer

1. **Select a Project**: Choose from built-in sample projects or upload your own ZIP file
2. **Color by Parameter**: Use the "Color by" dropdown to color-code data points by a parameter
3. **Sort Images**: Use the "Sort by" dropdown to sort images based on a parameter
4. **Explore Images**: Click on images to view details in the selected image panel
5. **Filter Data**: Use the parallel coordinates plot to filter data points by dragging on axes
6. **View Data Table**: Scroll down to see the complete data table

## Sample Projects

Design Explorer includes several sample projects to help you get started:

- **Daylight Factor**: Explore daylight simulation results
- **Box**: 3D box design variations
- **Box Without Images**: Parameter variations without images

## Creating Custom Projects

To create your own project, prepare a ZIP file with the following structure:

```
project-name/
├── data.csv          # Main data file
└── images/           # Image files referenced in data.csv
    ├── image1.png
    ├── image2.png
    └── ...
```

### Data CSV Format

The `data.csv` file should contain your design parameters and image references:

```csv
param1,param2,param3,img:Image
a,b,c,image1.png
d,e,f,image2.png
...
```

- Use `img:` prefix for image columns
- Use descriptive column names for better readability

## Technology Stack

- **Frontend**: Dash (Plotly), HTML, CSS, Bootstrap
- **Backend**: Python, Flask
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly Express

## Development

### Project Structure

```
design-explorer/
├── app/                  # Main application code
│   ├── callbacks/        # Dash callback functions
│   ├── containers/       # UI component containers
│   ├── assets/           # Static assets (CSS, images)
│   └── app.py            # Application entry point
├── README.md             # This file
├── README_CN.md          # Chinese README
└── requirements.txt      # Dependencies
```

### Adding New Features

1. Create a new branch for your feature
2. Implement your changes
3. Test thoroughly
4. Submit a pull request

### Running Tests

```bash
# Run tests (if available)
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Dash](https://dash.plotly.com/) and [Plotly](https://plotly.com/)
- Inspired by design optimization workflows
- Thanks to all contributors

## Contact

For questions or feedback, please open an issue on GitHub or contact the maintainers.

---

*Happy exploring!*