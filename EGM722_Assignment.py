import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, LineString, Point

#-------Import data and check epsg---------------------------------------------#
data_path = 'D:\\_MSc\\EGM722\\Github\\EGM722_Assignment\\data_files'

#Import the shapefiles as GeoPandas Geodataframe
lands = gpd.read_file(data_path+'\\land.shp')
rcv = gpd.read_file(data_path+'\\receivers.shp')
roads = gpd.read_file(data_path+'\\roads.shp')

#Display the EPSG Code of the data, and check if all has same projection
if lands.crs == rcv.crs == roads.crs:
    for i in lands.crs:
        print ('The EPSG code for the lands data: \'{}\''.format(lands.crs[i]))
    for i in lands.crs:
        print ('The EPSG code for the receviers data: \'{}\''.format(rcv.crs[i]))
    for i in lands.crs:
        print ('The EPSG code for the roads data: \'{}\''.format(roads.crs[i]))
else:
    print ('The data is not the same projection\n')

#-------Count number of receiver points, and number of lands-------------------#
print ('\nThere are ({}) land parcels within the project\'s area'.format(lands['geometry'].count()))
print ('There are ({}) receiver points within the project\'s area'.format(rcv['geometry'].count()))

#-------Intersect receviers with lands----------------------------------------#
