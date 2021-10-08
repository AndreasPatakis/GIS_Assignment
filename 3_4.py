from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
from sqlalchemy import create_engine
import geopandas as gpd
import numpy as np

from config import DB_CONFIG
from preprocess import cleanse

engine = create_engine(f'postgresql://{DB_CONFIG["user"]}:{DB_CONFIG["password"]}@{DB_CONFIG["host"]}:5432/{DB_CONFIG["database"]}')

NUM_OF_VESSELS = 1000000

traj_sql = f'''
SELECT timest, dates, mmsi, heading, speed, course, geom FROM vessels_points_jan
WHERE ST_X(ST_Centroid(ST_Transform(geom, 4326))) != 0 
OR ST_Y(ST_Centroid(ST_Transform(geom, 4326))) != 0 LIMIT {NUM_OF_VESSELS};
'''

print('Reading dataset from PostGIS...')
gdf = gpd.GeoDataFrame.from_postgis(traj_sql, engine, geom_col='geom')
print('Cleansing dataset...')
gdf = cleanse(gdf)

# Create input vector from longitude and latitude
X=np.column_stack((gdf.geom.x, gdf.geom.y))

print('Kmeans started...')
kmeans = KMeans(n_clusters = 3, random_state = 5,  max_iter = 400)
y_kmeans = kmeans.fit_predict(X)
print('Kmeans finished...')

k=gpd.GeoDataFrame(y_kmeans, columns=['hotspot'])
gdf=gdf.join(k)

print('Writing to PostGIS...')
gdf.rename(columns = {'geom':'geometry'}, inplace = True)
gdf.to_postgis('vessel_hot_spots', engine)
