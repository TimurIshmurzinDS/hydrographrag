python
   import geopandas as gpd
   import folium
   from shapely.geometry import Point
   from shapely import wkt

   # Load the shapefile and convert to CRS 'EPSG:4326'
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
   m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron', zoom_start=10)

   # Add the basin to the map using folium.GeoJson
   folium.GeoJson(basin, name='Basin', style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # If the context contains Coordinates (WKT), create a hardcoded list of dictionaries
   # coordinates = [{'name': 'Confluence Point', 'coordinates': wkt.loads('POINT(longitude latitude)')}]

   # For each coordinate, add a marker to the map
   # for point in coordinates:
   #     folium.Marker([point['coordinates'].y, point['coordinates'].x], popup=point['name']).add_to(m)

   # Save the final map
   m.save("171.html")