import geopandas as gpd
import cartopy.crs as ccrs
import matplotlib.pyplot as pplt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib_scalebar.scalebar import ScaleBar

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
    print ('Land Feature projection:{}, Roads Feature Projection:{}, Receivers Feature Projection:{}'
           .format(land.crs,roads.crs,rcv.crs))

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

#Update the number of receivers column
for i in land_clip.iterrows():
    land_clip['no_of_rcv'] = pt_poly_join.groupby(['land_id'])['station'].count()

#--------Calculate Compnsation per each property-------------------------------#
def compensation(x,y):
    """The user inputs the compensation value for agricultural & residential lands,
    the function then calculates the value of compensation according to the number of receivers
    inside each property and updates the Compensation field"""

    print ('\nThe compensation values for each land:')
    land_clip.loc[land_clip['land_type'] == 'agricultural', 'compensation'] = land_clip['no_of_rcv'] * x
    land_clip.loc[land_clip['land_type'] == 'residential', 'compensation'] = land_clip['no_of_rcv'] * y

    print (land_clip , '\n')
    #Create a csv file of all compensation values per property
    land_clip[['land_id', 'owner', 'compensation']].to_csv('Compensation.csv')

compensation(int(input('Enter Agricultural land compensation value:')),
             int(input('Enter Residential land compensation value:')))

#--------Buffer roads and clip receivers---------------------------------------#
def rcv_skips():
    """Creates a list of all Receivers within certain distance of roads
    and adds the result to a list, then create a Geodataframe and saves it as
    shapefile"""

    global skipped_rcv_gdf
    skipped_rcv = []
    dist = []

    #Enter the distance to be skipped around each road type
    dist1 = int(input('Enter the distance to be skipped around Main roads:'))
    dist2 = int(input('Enter the distance to be skipped around Secondary roads:'))

    #Iterate through road types and assign skip distances
    for rd_type in roads['road_type']:
        if rd_type == 'main':
            dist.append(dist1)
        elif rd_type == 'secondary':
            dist.append(dist2)

    #Append each receiver point within the search distance of roads to an empty list
    for pt in rcv.geometry:
        if (roads.geometry.distance(pt) <= [i for i in dist]).any():
            skipped_rcv.append(pt)

    print ('\nNumber or Receiver Skips: {}'.format(len(skipped_rcv)))

    #Create geodataframe of skipped receivers and export it as shapefile file
    skipped_rcv_gdf = gpd.GeoDataFrame(geometry=skipped_rcv)
    skipped_rcv_gdf.to_file('Skipped_rcv')

rcv_skips()

#--------plot map of lands & skips---------------------------------------------#
#Design the canvas
myFig = pplt.figure(figsize=(10, 8))
myCRS = ccrs.UTM(37)
ax = pplt.axes(projection=ccrs.Mercator())

#Plot the data
pplt.title("Land Parcels & Skipped Receivers", fontsize=20, color="black")
land.plot(ax=ax, alpha = 0.5, color = 'blue', label = 'Land',transform = myCRS)
rcv.plot(ax=ax,color = 'green', label = 'Receivers',transform = myCRS)
skipped_rcv_gdf.plot(ax=ax,color = 'red', label = 'Skipped Receivers',transform = myCRS)
roads.plot(ax=ax, color = 'orange', label = 'Roads',transform = myCRS)

#Create Legend shapes
legend_elements = [Line2D([0], [0], marker='o', color='w', label='Receiver',
                          markerfacecolor='g', markersize=10),
                   Line2D([], [], marker='o', color='w', label='Skipped Receiver',
                          markerfacecolor='r',markersize=10),
                   Line2D([0], [0], color='orange', lw=2, label='Roads'),
                   Patch(facecolor='blue', edgecolor='black',
                         label='Land', alpha = 0.5)]

ax.legend(handles=legend_elements, loc='upper right')

scalebar = ScaleBar(1, "m", length_fraction=0.25,location='lower left')
ax.add_artist(scalebar)

pplt.show()
