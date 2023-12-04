import numpy as np

def hex_to_rgb(hex_color):
    '''
    Converts a hex color to RGB.
    '''
    hex_color = hex_color.lstrip('#')
    return np.array([int(hex_color[i:i+2], 16) for i in (0, 2, 4)])