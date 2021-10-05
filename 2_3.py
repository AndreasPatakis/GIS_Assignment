import psycopg2
import psycopg2.extras
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

from config import DB_CONFIG

NUM_OF_VESSELS = 200000

conn = psycopg2.connect(**DB_CONFIG)
traj_sql = f'SELECT dates, mmsi, speed, geom FROM vessels_points_jan ORDER BY mmsi DESC, dates DESC LIMIT {NUM_OF_VESSELS}'
df = gpd.GeoDataFrame.from_postgis(traj_sql, conn, geom_col='geom').drop('geom', axis=1)

speed_stamps = df['speed']
speed_bins =[0] * 30

for stamp in speed_stamps:
    try:
        pos = int(stamp/10)
        if(pos >29):
            speed_bins[29] += 1
        else:
            speed_bins[pos] +=1
    except ValueError:
        continue

x_axis = []
for i in range(31):
    x_axis.append(i)

plt.figure('Speed per observation')
plt.hist(speed_bins,bins = x_axis,log=True , edgecolor = 'white')
plt.ylabel('Records')
plt.xlabel('km/h speed')
plt.title(f'Statistics for speed of vessels in {NUM_OF_VESSELS} records')
plt.xticks(np.arange(0,31,1))
plt.show()

conn.close()
