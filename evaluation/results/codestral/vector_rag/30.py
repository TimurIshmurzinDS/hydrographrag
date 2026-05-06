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

       # Hardcoded list of dictionaries for observation location
       observations = [{'name': '2 km above mouth of Prokhodnoy River', 'coordinates': wkt.loads('POINT (37.6184 55.7512)')}]

       # Add the observation location to the map
       for obs in observations:
           folium.Marker(location=[obs['coordinates'].y, obs['coordinates'].x], popup=obs['name']).add_to(m)

       # Assume we have a function get_current_discharge() that returns the current discharge of the Prokhodnaya River in m³/s
       current_discharge = get_current_discharge()

       # Assume the maximum allowable discharge without flooding risk is 1000 m³/s
       max_allowable_discharge = 1000

       # Calculate flood risk index
       flood_risk_index = current_discharge / max_allowable_discharge

       print(f'Flood Risk Index: {flood_risk_index}')

       # Save the final map
       m.save("30.html")