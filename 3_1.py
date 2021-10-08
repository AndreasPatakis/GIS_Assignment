import psycopg2
import psycopg2.extras
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point

from config import DB_CONFIG
from preprocess import cleanse
from utils import get_points

conn = psycopg2.connect(**DB_CONFIG)

NUM_OF_VESSELS = 1000

traj_sql = f'SELECT timest, dates, mmsi, heading, speed, course, geom FROM vessels_points_jan ORDER BY mmsi DESC, timest ASC LIMIT {NUM_OF_VESSELS}'

def segment_trajectories(points, time_interval = 12):
    trajectories = []
    trajectory = []
    for i in range(points.shape[0] - 1):
        minutes = (points.iloc[i+1]['timest'] - points.iloc[i]['timest']) / 60000

        if minutes > time_interval:
            if len(trajectory) > 3:
                trajectories.append(list(map(lambda s: (s.x, s.y), trajectory)))
            trajectory = []
        
        trajectory.append(points.iloc[i]['geom'])
    
    return trajectories

df = gpd.GeoDataFrame.from_postgis(traj_sql, conn, geom_col='geom')
df = cleanse(df)

vessel = df['mmsi'].iloc[8]
points = get_points(df, vessel)

trajectories = segment_trajectories(points)

# TODO Express as line