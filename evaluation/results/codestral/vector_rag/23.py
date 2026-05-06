python
       import geopandas as gpd
       import folium
       from shapely import wkt

       # Load the basin data
       basin = gpd.read_file(r"data/basin_data.shp")
       basin = basin.to_crs('EPSG:4326')

       # Initialize folium map
       m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron', zoom_start=10)

       # Add the basin to the map
       folium.GeoJson(basin['geometry'], name='Basin', style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

       # Hardcoded list of dictionaries for observation points (replace with actual data if available)
       observations = [{'name': 'Observation 1', 'geometry': wkt.loads('POINT (37.654890 55.752220)')},
                       {'name': 'Observation 2', 'geometry': wkt.loads('POINT (37.654890 55.752220)')}]

       # Add observation points to the map
       for obs in observations:
           folium.Marker(location=[obs['geometry'].y, obs['geometry'].x], popup=obs['name']).add_to(m)

       # Save the final map
       m.save("23.html")