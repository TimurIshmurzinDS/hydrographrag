python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the shapefile and convert to CRS 'EPSG:4326'
   basin_data = gpd.read_file(r"data/basin_data.shp")
   basin_data = basin_data.to_crs('EPSG:4326')

   # Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
   m = folium.Map(location=[basin_data.centroid.y.mean(), basin_data.centroid.x.mean()], tiles='CartoDB positron')

   # Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
   folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries containing coordinates (WKT) if available in the context
   observations = [{'name': 'Bayankol village observation 1', 'coordinates': 'POINT (69.358740 52.972040)'},
                   {'name': 'Bayankol village observation 2', 'coordinates': 'POINT (69.360120 52.971560)'},
                   {'name': 'Bayankol village observation 3', 'coordinates': 'POINT (69.361480 52.971080)'},
                   {'name': 'Bayankol village observation 4', 'coordinates': 'POINT (69.362840 52.970600)'}]

   # Add observations to the map as markers
   for obs in observations:
       coords = wkt.loads(obs['coordinates'])
       folium.Marker([coords.y, coords.x], popup=obs['name']).add_to(m)

   # Save the final map
   m.save("215.html")