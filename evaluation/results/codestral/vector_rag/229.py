python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the shapefile and convert to CRS 'EPSG:4326'
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
   m = folium.Map(location=[basin.centroid.y.mean(), basin.centroid.x.mean()], tiles='CartoDB positron')

   # Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries for rivers (WKT coordinates are not provided in the context)
   rivers = [{'name': 'Aksu River'}, {'name': 'Koksu River'}, {'name': 'Kishi Osek River'}]

   # Add rivers to the map (this is a placeholder, as WKT coordinates are not provided)
   for river in rivers:
       folium.Marker(location=[0, 0], popup=river['name']).add_to(m)

   # Save the final map
   m.save("229.html")