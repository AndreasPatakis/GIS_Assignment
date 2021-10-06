from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
from sqlalchemy import create_engine
import geopandas as gpd
import numpy as np

from config import DB_CONFIG

engine = create_engine(f'postgresql://{DB_CONFIG["user"]}:{DB_CONFIG["password"]}@{DB_CONFIG["host"]}:5432/{DB_CONFIG["database"]}')

traj_sql = f'''
SELECT mmsi, geom FROM vessels_points_jan
WHERE ST_X(ST_Centroid(ST_Transform(geom, 4326))) != 0 
OR ST_Y(ST_Centroid(ST_Transform(geom, 4326))) != 0;
'''

gdf = gpd.GeoDataFrame.from_postgis(traj_sql, engine, geom_col='geom')

# Create input vector from longitude and latitude
X=np.column_stack((gdf.geom.x, gdf.geom.y))

kmeans = KMeans(n_clusters = 3, random_state = 5,  max_iter = 400)
y_kmeans = kmeans.fit_predict(X)

k=gpd.GeoDataFrame(y_kmeans, columns=['hotspot'])
gdf=gdf.join(k)

gdf.to_postgis('vessel_hot_spots', engine)
