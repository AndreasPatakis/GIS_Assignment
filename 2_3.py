import psycopg2
import psycopg2.extras
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

conn = psycopg2.connect(
    host="localhost",
    database="gis_lab",
    user="postgres",
    password="andreasmc10")

print(conn)

traj_sql = 'SELECT * FROM vessels_points_jan limit 2000000'
df = gpd.GeoDataFrame.from_postgis(traj_sql, conn, geom_col='geom')

df.drop_duplicates(subset=['timest','mmsi'],inplace=True)

timest_mmsi = df[['dates','mmsi','speed']]
timest_mmsi = timest_mmsi.sort_values(by=['mmsi','dates'], ascending = [False,False])
mmsi = timest_mmsi.mmsi.unique()


speed_stamps = df['speed']
speed_bins =[0]*30

for stamp in speed_stamps:
    pos = int(stamp/10)
    if(pos >29):
        speed_bins[29] += 1
    else:
        speed_bins[pos] +=1

print(speed_bins)
x_axis = []
for i in range(31):
    x_axis.append(i)

plt.hist(speed_bins,bins = x_axis,log=True , edgecolor = 'white')
plt.ylabel('Records')
plt.xlabel('km/h speed');
plt.title('Statistics for speed of vessels in 2.000.000 records')
plt.xticks(np.arange(0,31,1))
plt.show()

conn.close()
