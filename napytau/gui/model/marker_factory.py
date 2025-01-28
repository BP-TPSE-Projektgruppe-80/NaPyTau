from matplotlib.path import Path
from matplotlib.markers import MarkerStyle


def generate_error_marker_path(error_amount: float) -> Path:
    """
    Create a path to describe how an error marker should be drawn around a data point
    """

    y_coord = error_amount / 2  # marker shape length depends on error amount

    verts = [  # Defines coordinates for the markers shape like this:
        (-0.5, y_coord),  # *--*--*        (-0.5, y)---(0, y)---(0.5, y)
        (0.5, y_coord),  # |                          |
        (0, y_coord),  # |                        (0,0)
        (0, -y_coord),  # |                          |
        (-0.5, -y_coord),  # *--*--*       (-0.5, -y)---(0, -y)---(0.5, -y)
        (0.5, -y_coord),
    ]

    # After defining coordinates of the shape we need instruction on how to connect
    # each point which each other to create the desired marker shape

    instructions = [
        Path.MOVETO,  # Move "pen" to point (first coord in 'verts' -> (-0.5, -y))
        Path.LINETO,  # Draw line towards second coord in 'verts' (0.5, -y)
        Path.MOVETO,  # Move "pen" to third point in 'verts'
        Path.LINETO,  # Draw line to fourth point in 'verts'
        Path.MOVETO,  # Move pen....
        Path.LINETO,  # Draw...
    ]

    return Path(verts, instructions)


def generate_marker(path: Path) -> MarkerStyle:
    """Creates new marker for the given path."""
    return MarkerStyle(path)
