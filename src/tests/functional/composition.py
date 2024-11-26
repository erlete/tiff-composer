import numpy as np
import rasterio
from rasterio.enums import Resampling

# Step 1: Define the size of the raster and synthetic data for bands
width, height = 10000, 10000  # Dimensions of the raster
bands = {
    'a': np.random.randint(0, 256, (height, width), dtype=np.uint8),
    'b': np.random.randint(0, 256, (height, width), dtype=np.uint8),
    'c': np.random.randint(0, 256, (height, width), dtype=np.uint8)
}

# Step 2: Create the TIFF file
output_file = 'multi_band_example.tif'
with rasterio.open(
    output_file,
    'w',
    driver='GTiff',
    height=height,
    width=width,
    count=len(bands),
    dtype=np.uint8,
    crs='+proj=latlong',
    transform=rasterio.transform.from_origin(-180, 90, 0.01, 0.01)
) as dst:
    for idx, (band_name, band_data) in enumerate(bands.items(), start=1):
        dst.write(band_data, idx)
        dst.set_band_description(idx, band_name)

print(f"Multi-band TIFF file created: {output_file}")

# Step 3: Open the TIFF file and display information
with rasterio.open(output_file) as src:
    print("\n=== File Information ===")
    print(f"Driver: {src.driver}")
    print(f"Width, Height: {src.width}, {src.height}")
    print(f"Number of Bands: {src.count}")
    print(f"Coordinate Reference System (CRS): {src.crs}")
    print(f"Bounds: {src.bounds}")
    print("\n=== Band Information ===")
    for idx in range(1, src.count + 1):
        print(f"Band {idx}: {src.descriptions[idx - 1]}")
        print(f"    Min: {src.read(idx).min()}, Max: {src.read(idx).max()}")
        print(f"    Data Type: {src.dtypes[idx - 1]}")

# Optional: Visualize band information (if required)
try:
    import matplotlib.pyplot as plt

    with rasterio.open(output_file) as src:
        fig, axs = plt.subplots(1, len(bands), figsize=(15, 5))
        for idx, ax in enumerate(axs, start=1):
            band_data = src.read(idx)
            ax.imshow(band_data, cmap='viridis')
            ax.set_title(f"Band {src.descriptions[idx - 1]}")
        plt.tight_layout()
        plt.show()

        # Plot all bands together
        fig, ax = plt.subplots(figsize=(10, 10))
        combined_image = np.dstack([src.read(idx)
                                   for idx in range(1, src.count + 1)])
        ax.imshow(combined_image)
        ax.set_title("Combined Bands")
        plt.show()

except ImportError:
    print("Matplotlib not installed. Skipping visualization.")
