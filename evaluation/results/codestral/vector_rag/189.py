python
       import geopandas as gpd
       import folium
       from shapely import wkt

       # Load the shapefile
       basin = gpd.read_file(r"data/basin_data.shp")
       basin = basin.to_crs('EPSG:4326')

       # Initialize folium map
       m = folium.Map(location=[basin.centroid.y.mean(), basin.centroid.x.mean()], tiles='CartoDB positron')

       # Add the basin to the map
       folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

       # Hardcoded list of dictionaries for Tauturgen village (if coordinates are available)
       observations = [{'name': 'Tauturgen village', 'coordinates': wkt.loads('POINT (longitude latitude)')}]

       # Add observations to the map
       for observation in observations:
           folium.Marker(location=[observation['coordinates'].y, observation['coordinates'].x], popup=observation['name']).add_to(m)

       # Save the final map
       m.save("189.html")