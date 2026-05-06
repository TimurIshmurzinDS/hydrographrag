import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin boundary shapefile
# Using raw string for path as per instructions
basin_df = gpd.read_file(r"data/basin_data.shp")
basin_df = basin_df.to_crs('EPSG:4326')

# 2. Initialize the map using the centroid of the basin
centroid = basin_df.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# 3. Add the basin boundary to the map
folium.GeoJson(
    basin_df, 
    fillColor='green', 
    color='darkgreen', 
    fillOpacity=0.2
).add_to(m)

# 4. Define river geometries (WKT)
# Since coordinates were not provided in the context, we define representative 
# geometries for Shynzhaly and Talgar to demonstrate the intersection logic.
rivers_data = [
    {
        "name": "Shynzhaly River",
        "wkt": "LINESTRING (77.450 43.150, 77.480 43.180, 77.510 43.200)"
    },
    {
        "name": "Talgar River",
        "wkt": "LINESTRING (77.400 43.220, 77.510 43.200, 77.600 43.150)"
    }
]

# Convert WKT to shapely objects
geometries = {r["name"]: wkt.loads(r["wkt"]) for r in rivers_data}

# 5. Calculate the spatial intersection of Shynzhaly and Talgar
river1 = geometries["Shynzhaly River"]
river2 = geometries["Talgar River"]
intersection_point = river1.intersection(river2)

# 6. Visualization of rivers and their intersection
for name, geom in geometries.items():
    # Convert shapely LineString to list of tuples for folium
    coords = [(p[1], p[0]) for p in geom.coords]
    folium.PolyLine(coords, tooltip=name, color="blue", weight=3).add_to(m)

if not intersection_point.is_empty:
    # Handle Point or MultiPoint result
    if intersection_point.geom_type == 'Point':
        pts = [(intersection_point.y, intersection_point.x)]
    else:
        pts = [(p.y, p.x) for p in intersection_point.geoms]
    
    for pt in pts:
        folium.Marker(
            location=pt, 
            popup="Intersection: Shynzhaly & Talgar", 
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)

# 7. Save the final map
m.save("169.html")