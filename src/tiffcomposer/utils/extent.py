
import numpy as np
import rasterio
from rasterio.windows import Window

from tiffcomposer.core.coordinates import GeoCoordinateExtent


def clip_tiff_to_extent(
    src: rasterio.io.DatasetReader,
    extent: GeoCoordinateExtent
) -> np.ndarray:
    """
    Clips a raster dataset (already opened) to a custom extent (in geographic coordinates).

    Args:
        src (rasterio.io.DatasetReader): The opened rasterio dataset (src).
        extent (tuple): The extent to clip to, specified as (left, right, bottom, top).
                        The coordinates are in (lon_min, lon_max, lat_min, lat_max).

    Returns:
        np.ndarray: The clipped data as a numpy array.
    """
    # Unpack the extent tuple
    left, bottom, right, top = extent.to_tuple()

    # Convert the geographic coordinates (left, right, bottom, top) to pixel/row/col
    transform = src.transform
    row_min, col_min = ~transform * (left, top)  # top-left corner
    row_max, col_max = ~transform * (right, bottom)  # bottom-right corner

    # Convert the row/col values to integers
    row_min, col_min = int(row_min), int(col_min)
    row_max, col_max = int(row_max), int(col_max)

    # Make sure that the row/col values are within image bounds
    row_min = max(0, row_min)
    col_min = max(0, col_min)
    row_max = min(src.height, row_max)
    col_max = min(src.width, col_max)

    # Create the window based on the row/col values
    window = Window(col_min, row_min, col_max - col_min, row_max - row_min)

    # Read the data from the window
    # Read the first band (use src.read() for multiple bands)
    clipped_data = src.read(1, window=window)

    return clipped_data


def get_population_density_in_extent(extent: GeoCoordinateExtent, src: rasterio.io.DatasetReader, mode: str = 'mean') -> float:
    """
    Extracts the population density from the raster within a given extent and returns the value
    based on the specified mode (mean, max, or min).

    Args:
        left (float): The left longitude of the extent (in degrees).
        right (float): The right longitude of the extent (in degrees).
        bottom (float): The bottom latitude of the extent (in degrees).
        top (float): The top latitude of the extent (in degrees).
        src (rasterio.io.DatasetReader): The opened rasterio dataset (src).
        mode (str): The operation to perform on the data: 'mean', 'max', or 'min'.

    Returns:
        float: The population density value based on the specified mode.
    """
    # Clip the data to the specified extent
    clipped_data = clip_tiff_to_extent(src, extent)

    # Remove the "no data" values (assuming a value of 0.0 is used for no data)
    clipped_data = clipped_data[clipped_data > 0]

    # Return the value based on the mode
    if mode == 'mean':
        return np.mean(clipped_data)
    elif mode == 'max':
        return np.max(clipped_data)
    elif mode == 'min':
        return np.min(clipped_data)
    else:
        raise ValueError("Mode must be 'mean', 'max', or 'min'")
