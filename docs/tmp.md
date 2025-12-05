Variable Name
Data Type
Length
Value Definition
Domain Values
THE_GEOM
STATION_KEY
STATION_ID
NAME
ROAD_NAME
FULL_NAME COMMON_ROAD_NAME SECONDARY_NAME ROAD_NAME_BASE ROAD_NAME_TYPE INTERSECTION DISTANCE_TO_INTERSECTION ROAD_NUMBER LINK_NUMBER
MAB_W AY_TYPE MAB_W AY_NUMBER MAB_IDENTIFIER
ROAD_FUNCTIONAL_HIERARCHY
ROAD_ON_TYPE
LANE_COUNT ROAD_CLASSIFICATION_TYPE ROAD_CLASSIFICATION_ADMIN
RMS_REGION
LGA
SUBURB
POST_CODE
DEVICE_TYPE HEAVY_VEHICLE_CHECKING_STATION PERMANENT_STATION VEHICLE_CLASSIFIER LAMBERT_EASTING LAMBERT_NORTHING WGS84_LATITUDE WGS84_LONGITUDE
QUALITY_RATING
Geometry
Number
String 51 String 71 String 8000 String 152 String 100 String 79 String 50 String 20 String 70 Number
String 7 String 4 String 20 String 10 String 5
String 100
String 50 String 100 String 100 String 100
String 20
String 40 String 40 String 12 String 100 Boolean
Boolean Boolean
Number Number Number Number
Number
WGS84 Point Geometry
Unique Station Key
The ID of the traffic collection station
Name of the road otherwise specified
Road name
Road name, cardinal direction from the intersection, and nearest intersecting road
Common (localised) road name
Cardinal direction from intersection and nearest intersecting road
Road name without street type
Street type
Nearest intersecting road
Distance in metres to nearest intersecting road RMS classified road number
RMS classified road-link number
MAB Road type: A, M, B
MAB number
MAB Road type and number
Local, Primary, Arterial, Motorway, Dedicated Bus way, Urban service lane, Sub-Arterial Road, Distributor Road
On Culvert, On Dam Wall, On Bridge, In Tunnel and On Ground
Number of lanes of road including Unknown Lanes, One Lane, and Two or More Lanes
Type of road classification e.g.
Freeway, Street, Deviation, Highway, Road Administration of road classification:
Regional, ,Local and State
RMS region locations:
Hunter, W estern, Southern, ACT , Northern, South West and Sydney
Local Government Area
NSW suburb
Postcode
Recording device type
0: Non Heavy Vehicle Checking Station 1: Heavy Vehicle Checking Station
0: Non-Permanent Station
1: Permanent Station
0: Non Vehicle Classifier 1: Vehicle Classifier
NSW Lambert Coordinates System NSW Lambert Coordinates System WGS84 Coordinate System WGS84 Coordinate System
4: One or more years of data for either one or both directions has been excluded for quality reasons 5: No data has been excluded due to quality
Refer 5.1
Refer 5.7
Refer 5.8
DIRECTION_SEQ
Number
0: BOTH
1: NORTH
3: EAST
5: SOUTH
7: WEST
9: NORTHBOUND AND SOUTHBOUND 10: EASTBOUND AND WESTBOUND
Refer 5.3