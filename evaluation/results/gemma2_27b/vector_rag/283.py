import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium map centered on the basin centroid
m = folium.Map(location=basin.centroid.values[0], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Example usage of compare() function (replace with actual data)
series1 = pd.Series([1, 2, 3], index=pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']))
series2 = pd.Series([2, 3, 4], index=pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']))

comparison_result = series1.compare(series2)
print(comparison_result)

# Save the map
m.save("283.html")