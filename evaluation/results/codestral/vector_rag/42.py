python
       import geopandas as gpd
       import folium
       from shapely import wkt

       # Load the shapefile and convert to CRS 'EPSG:4326'
       basin = gpd.read_file(r"data/basin_data.shp")
       basin = basin.to_crs('EPSG:4326')

       # Initialize folium map using the centroid of the shapefile
       m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron')

       # Add the basin to the map
       folium.GeoJson(basin['geometry'], style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

       # Hardcoded list of dictionaries representing agricultural activities (replace with actual data if available)
       activities = [{'coordinates': wkt.loads('POINT (55.751244 37.618423)'), 'water_quality_class': 'Poor', 'water_level_value': 0.8, 'water_consumption_valuem³s': 1000}]

       # Add activities to the map
       for activity in activities:
           color = 'red' if activity['water_quality_class'] == 'Poor' else 'blue'
           opacity = 1 - (activity['water_consumption_valuem³s'] / max([a['water_consumption_valuem³s'] for a in activities]))
           folium.CircleMarker(location=[activity['coordinates'].y, activity['coordinates'].x], radius=activity['water_level_value']*10, color=color, fill=True, fill_opacity=opacity).add_to(m)

       # Save the final map
       m.save("42.html")