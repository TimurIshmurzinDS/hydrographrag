python
       import geopandas as gpd
       import folium
       from shapely import wkt

       # Load the basin data
       basin_data = gpd.read_file(r"data/basin_data.shp")
       basin_data = basin_data.to_crs('EPSG:4326')

       # Initialize folium map with the centroid of the basin data
       m = folium.Map(location=[basin_data['geometry'].centroid.y.mean(), basin_data['geometry'].centroid.x.mean()], tiles='CartoDB positron')

       # Add the basin to the map
       folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

       # Hardcoded list of dictionaries representing water quality data at different points on the river Lepsi
       water_quality_data = [
           {'coordinates': wkt.loads('POINT (55.751244 37.618423)'), 'water_quality_class': 'A'},
           {'coordinates': wkt.loads('POINT (55.749044 37.620423)'), 'water_quality_class': 'B'},
           # Add more data points as needed
       ]

       # Define a function to assign colors based on water quality class
       def color_producer(water_quality_class):
           if water_quality_class == 'A':
               return 'green'
           elif water_quality_class == 'B':
               return 'yellow'
           else:
               return 'red'

       # Add water quality data points to the map
       for point in water_quality_data:
           folium.CircleMarker(location=[point['coordinates'].y, point['coordinates'].x], radius=10, color=color_producer(point['water_quality_class']), fill=True, fill_color=color_producer(point['water_quality_class'])).add_to(m)

       # Save the final map
       m.save("34.html")