import os

import matplotlib.pyplot as plt
import rasterio

from tiffcomposer.core.coordinates import GeoCoordinate, GeoCoordinateExtent
from tiffcomposer.utils.extent import get_population_density_in_extent
from tiffcomposer.utils.pixel import get_value_from_coordinates

FILE_PATH = os.path.join(os.path.dirname(__file__), 'esp_pd_2020_1km.tif')
MADRID = GeoCoordinate(40.4168, -3.7026)  # Madrid, Spain

# Open the TIFF file
with rasterio.open(FILE_PATH) as src:
    # Read the image data as a 2D array
    data = src.read(1)

    # Set any data value lower than 0 to 0
    data[data < 0] = 0

    print(src.crs)  # EPSG:4326
    print(src.bounds)  # Bounding box of the image

    # Plotting the image using matplotlib with latitude and longitude axes
    fig, ax = plt.subplots()
    img = ax.imshow(
        data,
        cmap='viridis',
        extent=(
            src.bounds.left,
            src.bounds.right,
            src.bounds.bottom,
            src.bounds.top
        )
    )
    plt.colorbar(img, ax=ax)  # Adds a colorbar to understand the value scale
    ax.set_title('Population Density')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    plt.show()


# Open the TIFF file to get the affine transform and image dimensions
with rasterio.open(FILE_PATH) as src:
    value = get_value_from_coordinates(MADRID, src, data)
    if value is not None:
        print(f"Population density at {MADRID}: {value} people/km^2")
    else:
        print("Coordinates are outside the image bounds.")


with rasterio.open(FILE_PATH) as src:
    extent_r = 1
    extent = GeoCoordinateExtent(
        GeoCoordinate(
            MADRID.latitude - extent_r,
            MADRID.longitude - extent_r
        ),
        GeoCoordinate(
            MADRID.latitude + extent_r,
            MADRID.longitude + extent_r
        )
    )

    mean_density = get_population_density_in_extent(
        extent,
        src,
        mode='mean'
    )
    print(f"Mean population density in the extent: {mean_density} people/km^2")

    max_density = get_population_density_in_extent(
        extent,
        src,
        mode='max'
    )
    print(f"Max population density in the extent: {max_density} people/km^2")

    min_density = get_population_density_in_extent(
        extent,
        src,
        mode='min'
    )
    print(f"Min population density in the extent: {min_density} people/km^2")
