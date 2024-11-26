from pprint import pprint

import rasterio
from rasterio.plot import show

# Function to extract and display extensive information about a TIFF file


def read_tiff(file_path, target_crs="EPSG:4326"):
    reprojected = False

    try:
        with rasterio.open(file_path) as src:
            print("\n=== General File Information ===")
            print(f"File: {file_path}")
            print(f"Driver: {src.driver}")
            print(f"Width, Height: {src.width}, {src.height}")
            print(f"Number of Bands: {src.count}")
            print(f"Coordinate Reference System (CRS): {src.crs}")
            print(f"Bounds: {src.bounds}")
            print(f"Transform: {src.transform}")

            print("\n=== Band Information ===")
            for idx in range(1, src.count + 1):
                band_data = src.read(idx)

                # Conver to target crs if necessary:
                if target_crs is not None and src.crs != target_crs:
                    band_data = src.read(
                        idx,
                        out_shape=(src.height, src.width),
                        resampling=rasterio.enums.Resampling.bilinear
                    )
                    reprojected = True
                    print(f"Band {idx} reprojected to {target_crs}")
                else:
                    print(f"Band {idx} not reprojected")

                # Replace nodata values with 0
                nodata_value = src.nodata
                if nodata_value is not None:
                    band_data = band_data.astype('float32')
                    band_data[band_data == nodata_value] = 0

                print(f"\nBand {idx}: {src.descriptions[idx - 1]}")
                print(f"    Data Type: {src.dtypes[idx - 1]}")
                print(f"    Min: {band_data.min()}, Max: {band_data.max()}")
                print(f"    Mean: {band_data.mean():.2f}, Std Dev: {
                      band_data.std():.2f}")

            print("\n=== Metadata ===")
            pprint(src.meta)
    except Exception as e:
        print(f"Error reading the TIFF file: {e}")

# Visualization function (optional)


def visualize_bands(file_path, target_crs="EPSG:4326"):
    try:
        import matplotlib.pyplot as plt

        with rasterio.open(file_path) as src:
            fig, axs = plt.subplots(1, src.count, figsize=(15, 5))
            for idx, ax in enumerate(axs, start=1):
                band_data = src.read(idx)
                show(band_data, ax=ax, cmap='gray', title=f"Band {
                     idx}: {src.descriptions[idx - 1]}")
            plt.tight_layout()
            plt.show()
    except ImportError:
        print("Matplotlib not installed. Skipping visualization.")
    except Exception as e:
        print(f"Error visualizing TIFF bands: {e}")


# Main execution
if __name__ == "__main__":
    import os

    files = (
        "esp_pd_2020_1km.tif",
        "terrain_view.tiff"
    )

    tiff_file = os.path.join(os.path.dirname(
        __file__), "data", files[1])  # Replace with your TIFF file path
    print(f"Reading TIFF file: {tiff_file}")
    read_tiff(tiff_file)

    print("\nVisualizing bands (if possible)...")
    visualize_bands(tiff_file)
