import numpy as np
import rasterio
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys

# Step 1: Check if an image file is passed
if len(sys.argv) > 1:
    image_file = sys.argv[1]  # The image file path is passed as an argument
else:
    print("Please provide a satellite image file as an argument.")
    sys.exit(1)

# Step 2: Load the image
with rasterio.open(image_file) as sat_data:
    width_in_projected_units = sat_data.bounds.right - sat_data.bounds.left
    height_in_projected_units = sat_data.bounds.top - sat_data.bounds.bottom
    print("Width: {}, Height: {}".format(width_in_projected_units, height_in_projected_units))
    print("Rows: {}, Columns: {}".format(sat_data.height, sat_data.width))

    # Step 3: Extract bands (assuming 3rd band is RED and 4th band is NIR)
    b, g, r, n = sat_data.read()  # Reading all 4 bands (b = blue, g = green, r = red, n = nir)

# Step 4: NDVI calculation
ndvi = (n.astype(float) - r.astype(float)) / (n + r)
print("NDVI calculated")

# Step 5: Normalize NDVI values to the range 0.1 to 1
ndvi_min = np.nanmin(ndvi)
ndvi_max = np.nanmax(ndvi)
ndvi_normalized = 0.1 + ((ndvi - ndvi_min) / (ndvi_max - ndvi_min)) * (1 - 0.1)

# Step 6: Create a mask for NDVI values above 0.8
high_ndvi_mask = ndvi_normalized > 0.8

# Step 7: Create a composite image using the green band (G) for display
green_image = g

# Normalize the green values to the range 0-255 for display
green_image_normalized = (green_image - green_image.min()) / (green_image.max() - green_image.min()) * 255
green_image_normalized = green_image_normalized.astype('uint8')

# Step 8: Plot the satellite image
fig, ax = plt.subplots()
ax.imshow(green_image_normalized, cmap='Greens')

# Step 9: Mark all positions with NDVI values above 0.8
rows, cols = np.where(high_ndvi_mask)
for row, col in zip(rows, cols):
    # Draw a rectangle (or any other marker) around each high NDVI position
    rect = patches.Rectangle((col, row), 1, 1, linewidth=1, edgecolor='red', facecolor='none')
    ax.add_patch(rect)

# Add a title and show the image
plt.title("Green Satellite Image with Marked NDVI > 0.8")
plt.show()

# Step 10: Save normalized NDVI result to a new GeoTIFF file
kwargs = sat_data.meta  # Get metadata from the original image
kwargs.update(dtype='float32', count=1)  # Update metadata for single-band NDVI

# Save the normalized NDVI image to a file
output_filename = 'normalized_high_ndvi.tif'
with rasterio.open(output_filename, 'w', **kwargs) as dst:
    dst.write(ndvi_normalized.astype('float32'), 1)

print(f"Normalized NDVI image for values above 0.8 saved as '{output_filename}'")
