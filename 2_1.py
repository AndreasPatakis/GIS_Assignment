import psycopg2
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

from config import DB_CONFIG

RECORDS_LIMIT = 50000
conn = psycopg2.connect(**DB_CONFIG)

if conn.closed == 0:
    print("Connected to DB")

all_points_sql = 'SELECT * FROM vessels_points_jan limit {}'.format(RECORDS_LIMIT)

all_points_gdf =  gpd.GeoDataFrame.from_postgis(all_points_sql, conn, geom_col='geom')


print(all_points_gdf.head())
