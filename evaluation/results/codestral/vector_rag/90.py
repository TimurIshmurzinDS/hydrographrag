python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the shapefile and convert to CRS 'EPSG:4326'
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium map using the centroid of the shapefile
   m = folium.Map(location=[basin.centroid.y.mean(), basin.centroid.x.mean()], tiles='CartoDB positron')

   # Add the basin to the map
   folium.GeoJson(basin, name='Basin', style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries for rivers (WKT coordinates should be provided in the context)
   rivers = [{'name': 'Temirlik River', 'wkt': 'POINT(...)'},
             {'name': 'Karaoy River', 'wkt': 'POINT(...)'},
             {'name': 'Baskan River', 'wkt': 'POINT(...)'}]

   # Add rivers to the map (assuming WKT coordinates are provided)
   for river in rivers:
       folium.Marker(location=wkt.loads(river['wkt']).coords[0], popup=river['name'], icon=folium.Icon(color='blue')).add_to(m)

   # Save the final map
   m.save("90.html")