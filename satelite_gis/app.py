import geopandas as gpd
from shapely.geometry import box
import rasterio
import numpy as np
import matplotlib.pyplot as plt

# Ladataan shapefile (esim. alueiden rajat)
shapefile = gpd.read_file('path_to_shapefile.shp')

# Esimerkki: Luodaan neliön muotoinen alue geometriaa varten
minx, miny, maxx, maxy = -73.0, 40.0, -72.0, 41.0
geom = box(minx, miny, maxx, maxy)

# Luodaan GeoDataFrame
gdf = gpd.GeoDataFrame({'geometry': [geom]}, crs="EPSG:4326")

# Visualisoidaan alue
gdf.plot()
plt.show()
# Ladataan kaksi kuvaa eri aikajaksoilta
with rasterio.open('path_to_image_1.tif') as src1:
    image1 = src1.read()
    
with rasterio.open('path_to_image_2.tif') as src2:
    image2 = src2.read()

# Lasketaan NDVI molemmista kuvista ja vertaillaan
ndvi1 = (image1[3].astype(float) - image1[0].astype(float)) / (image1[3] + image1[0])
ndvi2 = (image2[3].astype(float) - image2[0].astype(float)) / (image2[3] + image2[0])

# Visualisoidaan muutokset
ndvi_diff = ndvi2 - ndvi1
plt.imshow(ndvi_diff, cmap='coolwarm')
plt.title('NDVI-muutokset ajan myötä')
plt.colorbar()
plt.show()

# Ladataan satelliittikuva (esim. Landsat tai Sentinel)
with rasterio.open('path_to_image.tif') as src:
    image = src.read()  # Ladataan kaikki bändit
    profile = src.profile  # Kuvaustiedot (metadata)

# Kuvan visualisointi
plt.imshow(image[0], cmap='gray')  # Esimerkiksi ensimmäinen bändi (punainen)
plt.title('Satelliittikuva (punainen bändi)')
plt.show()
# Oletetaan, että punainen bändi on image[0] ja NIR (läheltä infrapunainen) on image[3]
red_band = image[0].astype(float)
nir_band = image[3].astype(float)

# Lasketaan NDVI
ndvi = (nir_band - red_band) / (nir_band + red_band)

# Visualisoidaan NDVI
plt.imshow(ndvi, cmap='RdYlGn')
plt.title('NDVI-indeksi')
plt.colorbar()
plt.show()
# Metsäkadon alueet: arvojen alle tietyn kynnysarvon (esim. -0.1)
def detect_deforestation(ndvi, threshold=-0.1):
    deforestation_mask = ndvi < threshold
    return deforestation_mask

deforestation = detect_deforestation(ndvi)

# Visualisoidaan metsäkatoalueet
plt.imshow(deforestation, cmap='hot')
plt.title('Metsäkatoalueet')
plt.show()

