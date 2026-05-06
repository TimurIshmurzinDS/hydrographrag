python
   import geopandas as gpd
   import folium
   from shapely.wkt import loads

   # Load the basin data
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium map
   m = folium.Map(location=[basin.centroid.y.mean(), basin.centroid.x.mean()], tiles='CartoDB positron')

   # Add the basin to the map
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries with river coordinates (WKT format)
   rivers = [
       {"name": "Shyzhyn River", "coordinates": "LINESTRING (37.564891 50.264891, 37.565891 50.265891)"},
       {"name": "Shilik River", "coordinates": "LINESTRING (37.566891 50.266891, 37.567891 50.267891)"}
   ]

   # Add rivers to the map
   for river in rivers:
       folium.PolyLine(locations=[loads(river["coordinates"]).coords], color="blue", weight=2, opacity=1).add_to(m)

   # Save the final map
   m.save("157.html")