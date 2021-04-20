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
# To fetch (all) the GPS points
print(conn)

traj_sql = 'SELECT * FROM vessels_points_jan limit 50000;'

df = gpd.GeoDataFrame.from_postgis(traj_sql, conn, geom_col='geom')

timest_mmsi = df[['dates','mmsi']]
timest_mmsi = timest_mmsi.sort_values(by=['mmsi','dates'], ascending = [False,False])
mmsi = timest_mmsi.mmsi.unique()

one_vessel = timest_mmsi[timest_mmsi['mmsi'] == 249226000]


less_than = [0]*50

vessel_stamps = []
for vessel in mmsi:
    vessel_stamps.append(timest_mmsi[timest_mmsi['mmsi'] == vessel])

for stamps in vessel_stamps:
    max_i = len(stamps.dates) -1
    for i,stamp in enumerate(stamps.dates):
        if(max_i < 1):
            pass
        else:
            days_diff = (stamps.iloc[i].dates - stamps.iloc[i+1].dates).days
            if(days_diff == 0):
                sec = (stamps.iloc[i].dates - stamps.iloc[i+1].dates).seconds
                pos = int(sec/5)
                if(pos>=49):
                    less_than[49] +=1
                else:
                    less_than[pos] +=1
            else:
                pass
        if(i == max_i -1):
            break;


#PLOT
x_axis = []
for i in range(0,51):
    x_axis.append(i*5)




plt.hist(less_than,log=True ,bins = x_axis, edgecolor = 'white')
plt.ylabel('Records')
plt.xlabel('Seconds');
plt.xticks(np.arange(0,255,5))
plt.show()

conn.close()
