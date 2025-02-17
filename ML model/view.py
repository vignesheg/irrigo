from osgeo import gdal
import matplotlib.pyplot as plt

# Path to your multispectral .tif file
file_path = 'multispectral.tif'

# Open the .tif file
dataset = gdal.Open(file_path)

# Extract the number of bands (images)
num_bands = dataset.RasterCount

# Initialize a figure for displaying all bands
fig, axes = plt.subplots(1, num_bands, figsize=(15, 5))

# Iterate through each band and plot it
for i in range(1, num_bands + 1):
    band = dataset.GetRasterBand(i).ReadAsArray()
    ax = axes[i-1] if num_bands > 1 else axes
    ax.imshow(band, cmap='gray')
    ax.set_title(f'Band {i}')
    ax.axis('off')

plt.tight_layout()
plt.show()
