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

   # Hardcoded list of dictionaries containing river coordinates (WKT)
   rivers = [
       {"name": "Bayankol River", "coordinates": "POINT (73.123456 55.123456)"},
       {"name": "Shilik River", "coordinates": "POINT (73.678901 55.678901)"}
   ]

   # Add rivers to the map
   for river in rivers:
       folium.Marker(location=wkt.loads(river["coordinates"]).coords[0], popup=river["name"]).add_to(m)

   # Save the final map
   m.save("130.html")