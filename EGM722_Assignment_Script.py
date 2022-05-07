import geopandas as gpd
import cartopy.crs as ccrs
import matplotlib.pyplot as pplt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib_scalebar.scalebar import ScaleBar

#-------Set the raw  path------------------------------------------------------#
data_path = 'D:\\_MSc\\EGM722\\Github\\EGM722_Assignment\\data_files'

#Import the shapefiles as GeoPandas Geodataframe
property = gpd.read_file(data_path + '\\properties.shp')
rcv = gpd.read_file(data_path + '\\receivers.shp')
roads = gpd.read_file(data_path + '\\roads.shp')

#Display the EPSG Code of the data, and check if all has same projection
if property.crs == rcv.crs == roads.crs:
    print ('All features are of coordinate system {}'.format(property.crs))
    pass
else:
    print ('Data will be reprojected as 1 or more features had mismatching projection')
    epsg_code = int((input('Enter the EPSG Code for the area: ')))#32639 for this data
    property = property.to_crs(epsg=epsg_code)
    roads = roads.to_crs(epsg=epsg_code)
    rcv = rcv.to_crs(epsg=epsg_code)
    print('Properties Feature projection:{}\nRoads Feature Projection:{}\nReceivers Feature Projection:{}'
          .format(property.crs, roads.crs, rcv.crs))

#-------Count number of receiver points, and number of properties--------------#
print('\nThere are ({}) properties within the project\'s area'.format(property['geometry'].count()))
print('There are total ({}) receiver points within the project\'s area\n'.format(rcv['geometry'].count()))

#-------Check if receviers Intersect  with properties--------------------------#
def point_inside_shape(point, polygon):
    """The function checks if the receivers intersect with properties.

     The function intersects the properties & receivers datasets,
     and count how many are inside each property"""

    global pt_poly_join
    pt_poly_join = gpd.sjoin(property, rcv, how='inner', lsuffix='left', rsuffix='right')
    pt_poly_count = pt_poly_join['geometry'].count()

    if pt_poly_count==0:
        print('No receivers within the properties')
    else:
        print('Below are the number of receivers intersecting each properties:')
        print(pt_poly_join.groupby(['land_id','land_type'])['station'].count())

point_inside_shape(rcv, property)

#--------Clip receivers with properties layer & create clipped layer-----------#
properties_clipped = gpd.clip(property, rcv)

#--------Add fields to the newely created layer--------------------------------#
properties_clipped.insert(len(properties_clipped.columns), 'no_of_rcv', 0)
properties_clipped.insert(len(properties_clipped.columns), 'compensation', 0)

#Update the number of receivers column
for i in properties_clipped.iterrows():
    properties_clipped['no_of_rcv'] = pt_poly_join.groupby(['land_id'])['station'].count()

#--------Calculate Compnsation per each property-------------------------------#
def compensation(x,y):
    """The function calculates the compensation per each property.

    The user inputs the compensation value for agricultural & residential properties,
    the function then calculates the value of compensation according to the number of receivers
    inside each property and updates the Compensation field, outputs result as csv"""

    print('\nThe compensation values for each property:')
    #Delete NaN values rows
    properties_clipped.dropna(inplace=True)

    #Calculate compensation per land type
    properties_clipped.loc[properties_clipped['land_type'] == 'agricultural', 'compensation'] = properties_clipped['no_of_rcv'] * x
    properties_clipped.loc[properties_clipped['land_type'] == 'residential', 'compensation'] = properties_clipped['no_of_rcv'] * y

    print(properties_clipped, '\n')

    #Create a csv file of all compensation values per property
    properties_clipped[['land_id', 'owner', 'compensation']].to_csv('Compensation.csv')

compensation(int(input('\nEnter Agricultural property compensation value per sensor:')),
             int(input('Enter Residential property compensation value per sensor:')))

#--------Buffer roads and clip receivers---------------------------------------#
def rcv_skips():
    """The function identifies skipped receivers from specific distance from roads.

    Creates a list of all Receivers within user buffer distance of roads according to
    road type, and adds the result to a list, then create a Geodataframe and saves it as
    shapefile"""

    global main_roads_buffer
    global secondary_roads_buffer
    global skipped_rcv_gdf

    skipped_rcv = []
    dist = []

    #Enter the distance to be skipped around each road type
    dist1 = int(input('Enter the distance to be skipped around Main roads:'))
    dist2 = int(input('Enter the distance to be skipped around Secondary roads:'))

    #Create main and secondary roads buffer features
    main_roads = roads[roads['road_type'] == 'main']
    main_roads_buffer = main_roads.geometry.buffer(dist1)
    main_roads_buffer.to_file('main_roads_buffer')
    secondary_roads = roads[roads['road_type'] == 'secondary']
    secondary_roads_buffer = secondary_roads.geometry.buffer(dist2)
    secondary_roads_buffer.to_file('secondary_roads_buffer')

    #Iterate through road types and assign skip distances to a list
    for rd_type in roads['road_type']:
        if rd_type == 'main':
            dist.append(dist1)
        elif rd_type == 'secondary':
            dist.append(dist2)

    #Append each receiver point within the search distance of roads to an empty list
    for pt in rcv.geometry:
        if (roads.geometry.distance(pt) <= [i for i in dist]).any():
            skipped_rcv.append(pt)
            
    print('\nNumber or Receiver Skips: {}'.format(len(skipped_rcv)))

    #Create geodataframe of skipped receivers and export it as shapefile file

    skipped_rcv_gdf = gpd.GeoDataFrame(geometry=skipped_rcv)
    skipped_rcv_gdf.to_file('skipped_rcv')

rcv_skips()

#--------plot map of lands & skips---------------------------------------------#
#Design the canvas
myFig = pplt.figure(figsize=(10, 8))
myCRS = ccrs.UTM(39)
ax = pplt.axes(projection=ccrs.Mercator())

#Plot the data
pplt.title("Properties & Skipped Receivers", fontsize=20, color="black")
property.plot(ax=ax, alpha = 0.5, color ='blue', transform = myCRS)
main_roads_buffer.plot(ax=ax, alpha = 0.5, color ='red', transform = myCRS)
secondary_roads_buffer.plot(ax=ax, alpha = 0.5, color ='yellow', transform = myCRS)
rcv.plot(ax=ax,color = 'green', transform = myCRS)
skipped_rcv_gdf.plot(ax=ax,color = 'red', transform = myCRS)
roads.plot(ax=ax, color = 'black', transform = myCRS)

#Create Legend shapes
legend_elements = [Line2D([0], [0], marker='o', color='w', label='Receiver',
                          markerfacecolor='g', markersize=10),
                   Line2D([], [], marker='o', color='w', label='Skipped Receiver',
                          markerfacecolor='r',markersize=10),
                   Line2D([0], [0], color='black', lw=2, label='Roads'),
                   Patch(facecolor='blue', edgecolor='black',
                         label='Property', alpha = 0.5),
                   Patch(facecolor='red', edgecolor='black',
                         label='Main Roads Buffer', alpha=0.5),
                   Patch(facecolor='yellow', edgecolor='black',
                         label='Secondary Roads Buffer', alpha=0.5)
                   ]

ax.legend(handles=legend_elements, loc='upper right')

#Create and add scalebar
scalebar = ScaleBar(1, "m", length_fraction=0.25,location='lower left')
ax.add_artist(scalebar)

pplt.savefig('Project_Map.png', dpi=300, bbox_inches='tight')

pplt.show()
