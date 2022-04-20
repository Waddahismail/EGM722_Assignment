import matplotlib as mplt
import geopandas as gpd
import matplotlib.pyplot as pplt
import cartopy.crs as ccrs
from cartopy.feature import ShapelyFeature
import numpy as np

#-------Set the data path------------------------------------------------------#
data_path = 'D:\\_MSc\\EGM722\\Github\\EGM722_Assignment\\data_files'

#Import the shapefiles as GeoPandas Geodataframe
land = gpd.read_file(data_path + '\\land.shp')
rcv = gpd.read_file(data_path+'\\receivers.shp')
roads = gpd.read_file(data_path+'\\roads.shp')

#Display the EPSG Code of the data, and check if all has same projection
if land.crs == rcv.crs == roads.crs:
    print ('The EPSG code for the lands, receivers and roads data: \'{}\''.format(land.crs))
else:
    print ('The data is not the same projection\n')

#-------Count number of receiver points, and number of lands-------------------#
print ('\nThere are ({}) land parcels within the project\'s area'.format(land['geometry'].count()))
print ('There are total ({}) receiver points within the project\'s area\n'.format(rcv['geometry'].count()))

#-------Check if receviers Intersect  with lands-------------------------------#
def point_inside_shape(point, polygon):
    """The function checks if the receivers intersect with land
    parcels, and count how many are inside each property"""
    global pt_poly_join
    pt_poly_join = gpd.sjoin(land, rcv, how='inner', lsuffix='left', rsuffix='right')
    pt_poly_count = pt_poly_join['geometry'].count()

    if pt_poly_count==0:
        print ('No receivers within the properties')
    else:
        print ('Below are the number of receivers intersecting each land parcel:')
        print (pt_poly_join.groupby(['land_id','land_type'])['station'].count())

point_inside_shape(rcv,land)

#--------Clip receivers with land layer----------------------------------------#
land_clip = gpd.clip(land, rcv)
land_clip.insert(len(land_clip.columns), 'no_of_rcv',0)
land_clip.insert(len(land_clip.columns), 'compensation',0)
for i in land_clip.iterrows():
    land_clip['no_of_rcv'] = pt_poly_join.groupby(['land_id'])['station'].count()

#--------Calculate Compnsation-------------------------------------------------#
def compensation(x,y):
    """ """
    print ('\nThe compensation values for each land:')
    land_clip.loc[land_clip['land_type'] == 'agricultural', 'compensation'] = land_clip['no_of_rcv'] * x
    land_clip.loc[land_clip['land_type'] == 'residential', 'compensation'] = land_clip['no_of_rcv'] * y

    print (land_clip , '\n')
    land_clip[['land_id', 'owner_id', 'compensation']].to_csv('Compensation.csv')
compensation(100,400)

#--------Buffer roads and clip receivers---------------------------------------#
def rcv_skips(dist):
    """Creates a list of all Receivers within certain distance of roads
    and adds the result to a list, then create a Geodataframe and saves it as
    shapefile"""

    global skipped_rcv_gdf
    skipped_rcv = []
    for pt in rcv.geometry:
        if (roads.geometry.distance(pt) <= dist).any():
            skipped_rcv.append(pt)

    print ('Number or Receiver Skips: {}'.format(len(skipped_rcv)))

    skipped_rcv_gdf = gpd.GeoDataFrame(geometry=skipped_rcv)
    skipped_rcv_gdf.to_file('Skipped_rcv')

rcv_skips(50)

#--------plot map of lands & skips---------------------------------------------#
myFig = pplt.figure(figsize=(10, 8))
myCRS = ccrs.UTM(37)
ax = pplt.axes(projection=ccrs.Mercator())

pplt.title("Land Parcels & Skipped Receivers", fontsize=20, color="black")


land.plot(ax=ax, alpha = 0.2, color = 'blue', label = 'Land')

rcv.plot(ax=ax,color = 'green', label = 'Receivers')
skipped_rcv_gdf.plot(ax=ax,color = 'red', label = 'Skipped Receivers')
roads.plot(ax=ax, color = 'orange', label = 'Roads')

handles, labels = pplt.gca().get_legend_handles_labels()

pplt.legend(handles=handles, labels=labels)
pplt.show()
