import psycopg2
import psycopg2.extras
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine
from shapely.geometry import Point, LineString
from shapely.ops import transform
from functools import partial
import pyproj

from config import DB_CONFIG
from preprocess import cleanse, calculate_bearing
from utils import get_points

engine = create_engine(f'postgresql://{DB_CONFIG["user"]}:{DB_CONFIG["password"]}@{DB_CONFIG["host"]}:5433/{DB_CONFIG["database"]}')

NUM_OF_VESSELS = 10000
ANGLE_THRESHOLD = 60

traj_sql = f'SELECT timest, dates, mmsi, heading, speed, course, geom FROM vessels_points_jan_new ORDER BY mmsi DESC, timest ASC LIMIT {NUM_OF_VESSELS}'


def segment_trajectories(points, time_interval = 12):

    trajectories = []
    trajectory = []
    date = 0
    dates = []
    
    for i in range(points.shape[0] - 1):
        angle = points.iloc[i+1]['heading'] - points.iloc[i]['heading']

        if abs(angle) > ANGLE_THRESHOLD:
            if len(trajectory) > 1:
                trajectories.append(trajectory)
                dates.append([date,points.iloc[i-1]['dates']])
            date = 0
            trajectory = []

        trajectory.append(points.iloc[i]['geom'])
        if not date:
            date = points.iloc[i]['dates']

    return trajectories, dates

df = gpd.GeoDataFrame.from_postgis(traj_sql, engine, geom_col='geom')
df = cleanse(df)
df = df[df['heading'] != 0]
df = df[df['speed'] != 0]

lines = []

project = partial(
    pyproj.transform,
    pyproj.Proj('EPSG:4326'),
    pyproj.Proj('EPSG:4326'))

for i,vessel in enumerate(df['mmsi'].unique()):
    points = get_points(df, vessel)
    trajectories, dates = segment_trajectories(points)
    for i,trajectory in enumerate(trajectories):
        lines.append((vessel,dates[i][0],dates[i][1],len(trajectory), transform(project,LineString(trajectory))))
    print('Trajectories for {}/{} vessels calculated successfully'.format(i+1,len(df['mmsi'].unique())))

gdf = gpd.GeoDataFrame(lines, columns=('mmsi','starting_on','ending_on','points' ,'geometry'))
gdf.to_postgis('segmented_trajectories3', engine)
