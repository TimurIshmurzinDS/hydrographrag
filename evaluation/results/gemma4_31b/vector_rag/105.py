import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin boundary shapefile
# Using raw string for path as per critical instructions
basin_df = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 (EPSG:4326) for compatibility with folium
basin_df = basin_df.to_crs('EPSG:4326')

# 2. Initialize the map
# Calculate the centroid of the basin to center the map
centroid = basin_df.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# 3. Add the basin boundary to the map
folium.GeoJson(
    basin_df,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    name='Basin Boundary'
).add_to(m)

# 4. Handle coordinates from context
# The context mentions Ulken Almaty River and observations 1.1km above the lake.
# Since specific WKT coordinates were not provided in the text context, 
# we define the identified entity logic here.
entities = [
    {"name": "Ulken Almaty River", "type": "HY_HydroFeature"},
    {"name": "Observation Point (1.1km above Lake)", "type": "Observation"}
]

# Note: If WKT coordinates were present in the context, they would be added as folium.Marker here.
# Example structure for future coordinate additions:
# for entity in hardcoded_coords_list:
#     folium.Marker([entity['lat'], entity['lon']], popup=entity['name']).add_to(m)

# 5. Save the final map strictly as 105.html
m.save("105.html")