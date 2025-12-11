"""Module for color scheme definitions and utilities."""

# Define the color schemes as RGB values
def get_color_schemes():
    """Return all available color schemes."""
    return {
        "Original": {
            "name": "Original",
            "colors": [
                (75, 107, 169),
                (115, 147, 202),
                (170, 200, 247),
                (193, 213, 208),
                (245, 239, 103),
                (252, 230, 74),
                (239, 156, 21),
                (234, 123, 0),
                (234, 74, 0),
                (234, 38, 0)
            ]
        },
        "Nuanced": {
            "name": "Nuanced",
            "colors": [
                (49, 54, 149),
                (69, 117, 180),
                (116, 173, 209),
                (171, 217, 233),
                (224, 243, 248),
                (255, 255, 191),
                (254, 224, 144),
                (253, 174, 97),
                (244, 109, 67),
                (215, 48, 39),
                (165, 0, 38)
            ]
        },
        "Multi-Colored": {
            "name": "Multi-Colored",
            "colors": [
                (4, 25, 145),
                (7, 48, 224),
                (7, 88, 255),
                (1, 232, 255),
                (97, 246, 156),
                (166, 249, 86),
                (254, 244, 1),
                (255, 121, 0),
                (239, 39, 0),
                (138, 17, 0)
            ]
        },
        "Parula": {
            "name": "Parula",
            "colors": [
                (52, 62, 175),
                (2, 99, 225),
                (7, 155, 207),
                (36, 180, 170),
                (107, 190, 130),
                (232, 185, 78),
                (252, 203, 47),
                (248, 250, 13)
            ]
        }
    }


def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color string."""
    return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'


def sample_color_scheme(color_scheme, value, min_value, max_value):
    """Sample a color from the given color scheme based on a normalized value."""
    # Normalize the value to 0-1 range
    normalized = (value - min_value) / (max_value - min_value) if max_value > min_value else 0
    
    # Get the colors from the scheme
    colors = color_scheme['colors']
    num_colors = len(colors)
    
    # Calculate the index
    index = int(normalized * (num_colors - 1))
    # Ensure index is within bounds
    index = max(0, min(index, num_colors - 1))
    
    # Return the hex color
    return rgb_to_hex(colors[index])


def get_default_color_scheme():
    """Return the default color scheme."""
    return "Original"
