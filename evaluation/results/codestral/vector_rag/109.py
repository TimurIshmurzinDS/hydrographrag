python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the shapefile
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium map
   m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron')

   # Add the basin to the map
   folium.GeoJson(basin, name='Basin', style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries for rivers (replace with actual data)
   rivers = [
       {"name": "Byzhy River", "flow_rate": None},
       {"name": "Lepsy River", "flow_rate": None},
       # Add other rivers here...
   ]

   # Save the final map
   m.save("109.html")