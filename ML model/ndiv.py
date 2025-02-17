
import math
import numpy
import rasterio
import matplotlib.pyplot as plt

image_file = 'multispectral.tif'
sat_data = rasterio.open(image_file)
width_in_projected_units = sat_data.bounds.right - sat_data.bounds.left
height_in_projected_units = sat_data.bounds.top - sat_data.bounds.bottom
print("Width: {}, Height: {}".format(width_in_projected_units, height_in_projected_units))
#prints the shape of data and data
sat_data.shape
print(sat_data)

print("Rows: {}, Columns: {}".format(sat_data.height, sat_data.width))
row_min = 0
col_min = 0
row_max = sat_data.height - 1
col_max = sat_data.width - 1
topleft = sat_data.transform * (row_min, col_min)
botright = sat_data.transform * (row_max, col_max)
print("Top left corner coordinates: {}".format(topleft))
print("Bottom right corner coordinates: {}".format(botright))


print(sat_data.count)

#the indices will be 4 beacuse it has 4 dimeansions
print(sat_data.indexes)

#r is assigned corresponding to red and n corresponds to the infrared 
b, g, r, n = sat_data.read()

fig = plt.imshow(b)
plt.show()
fig = plt.imshow(g)
fig.set_cmap('gist_earth')
plt.show()

fig = plt.imshow(r)
fig.set_cmap('inferno')
plt.colorbar()
plt.show()

fig = plt.imshow(n)
fig.set_cmap('winter')
plt.colorbar()
plt.show()

filename = 'multispectral.tif'
with rasterio.open(filename) as src: #reads 3rd dimension
    band_red = src.read(3)
with rasterio.open(filename) as src: #reads 4th dimesion
    band_nir = src.read(4)

numpy.seterr(divide='ignore', invalid='ignore')


ndvi = (band_nir.astype(float) - band_red.astype(float)) / (band_nir + band_red) #formula for ndvi
print("NDVI: ",ndvi)

print(numpy.nanmin(ndvi)) 
print(numpy.nanmax(ndvi))

meta = src.meta
print(meta)


ndvi_dtype = ndvi.dtype
print(ndvi_dtype)


kwargs = meta


kwargs.update(dtype=ndvi_dtype)


kwargs.update(count=1)


with rasterio.open('ForBhawana.tif', 'w', **kwargs) as dst:
        dst.write(ndvi, 1)

from matplotlib import colors

class MidpointNormalize(colors.Normalize):
   
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
       
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return numpy.ma.masked_array(numpy.interp(value, x, y), numpy.isnan(value))


min=numpy.nanmin(ndvi)
max=numpy.nanmax(ndvi)

mid=0.1

colormap = plt.cm.RdYlGn 
norm = MidpointNormalize(vmin=min, vmax=max, midpoint=mid)
fig = plt.figure(figsize=(20,10))

ax = fig.add_subplot(111)
cbar_plot = ax.imshow(ndvi, cmap=colormap, vmin=min, vmax=max, norm=norm)
ax.axis('off')
ax.set_title('Normalized Difference Vegetation Index', fontsize=17, fontweight='bold')

cbar = fig.colorbar(cbar_plot, orientation='horizontal', shrink=0.65)

fig.savefig("ndvi-image.png", dpi=200, bbox_inches='tight', pad_inches=0.7)

plt.show()

fig2 = plt.figure(figsize=(20,10))
ax = fig2.add_subplot(111)


plt.title("NDVI Histogram", fontsize=18, fontweight='bold')
plt.xlabel("NDVI values", fontsize=14)
plt.ylabel("Number of pixels", fontsize=14)



x = ndvi[~numpy.isnan(ndvi)]
color = 'g'
ax.hist(x,bins=30,color=color,histtype='bar', ec='black')
plt.show()