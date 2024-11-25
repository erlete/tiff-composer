
import numpy as np
import rasterio

from ..core.coordinates import GeoCoordinate


def get_value_from_coordinates(
    coordinate: GeoCoordinate,
    src: rasterio.io.DatasetReader,
    data: np.ndarray
) -> float | None:
    # Get the transformation from pixel coordinates to geographic coordinates
    transform = src.transform

    # Convert lat, lon to image row, col
    # The inverse of the affine transform to map lat, lon to pixel coordinates
    col, row = ~transform * coordinate.inverted.to_tuple()

    # Check if the coordinates are inside the image bounds
    if 0 <= col < src.width and 0 <= row < src.height:
        # Return the value in the image at the specified coordinates
        pixel_value = data[int(row), int(col)]
        return pixel_value
    else:
        # Coordinates are outside the image bounds
        return None
