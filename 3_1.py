import psycopg2
import psycopg2.extras
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point


#We choose to define a trajectory, in it's general form, by having the hypothesis
#that a journey of a vessel starts and stops in the ports. Then each of these trajectories
#will be devided in sub trajectories(trajectory segmentation) based on the time intervals
#that we will set.

#p1: lat:37.9474889 lon:23.6363779
#select st_buffer(st_geomfromtext('point(23.6363779 37.9474889)',4326),0.02)
conn = psycopg2.connect(
    host="localhost",
    database="gis_lab",
    user="postgres",
    password="andreasmc10")

print(conn)


p1 = Point(23.6363779, 37.9474889)
dfp = pd.DataFrame({'point': [1]})
gdf = gpd.GeoDataFrame(dfp, geometry = [p1])

gdf['geometry'] = gdf.geometry.buffer(0.02)
piraeus_port = gdf['geometry']
print(piraeus_port)


#traj_sql = 'SELECT * FROM vessels_points_jan limit 10000'
#df = gpd.GeoDataFrame.from_postgis(traj_sql, conn, geom_col='geom')

#vessels_in_port =
