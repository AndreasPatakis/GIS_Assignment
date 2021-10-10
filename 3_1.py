import psycopg2
import psycopg2.extras
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine
from shapely.geometry import Point, LineString

from config import DB_CONFIG
from preprocess import cleanse, calculate_bearing
from utils import get_points

engine = create_engine(f'postgresql://{DB_CONFIG["user"]}:{DB_CONFIG["password"]}@{DB_CONFIG["host"]}:5432/{DB_CONFIG["database"]}')

NUM_OF_VESSELS = 50000
ANGLE_THRESHOLD = 60

traj_sql = f'SELECT timest, dates, mmsi, heading, speed, course, geom FROM vessels_points_jan ORDER BY mmsi DESC, timest ASC LIMIT {NUM_OF_VESSELS}'

def segment_trajectories(points, time_interval = 12):

    trajectories = []
    trajectory = []
    for i in range(points.shape[0] - 1):
        angle = points.iloc[i+1]['heading'] - points.iloc[i]['heading']

        if abs(angle) > ANGLE_THRESHOLD:
            trajectories.append(trajectory)
            trajectory = []
        
        trajectory.append(points.iloc[i]['geom'])
    
    return trajectories

df = gpd.GeoDataFrame.from_postgis(traj_sql, engine, geom_col='geom')
df = cleanse(df)
df = df[df['heading'] != 0]
df = df[df['speed'] != 0]

lines = []

for vessel in df['mmsi'].unique():
    points = get_points(df, vessel)
    trajectories = segment_trajectories(points)

    for trajectory in filter(lambda t: len(t) > 1, trajectories):
        lines.append((vessel, LineString(trajectory)))

gdf = gpd.GeoDataFrame(lines, columns=('mmsi', 'geometry'))
gdf.to_postgis('segmented_trajectories', engine)
