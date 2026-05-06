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
     folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

     # Hardcoded list of tributaries and their coordinates (WKT format)
     tributaries = [
         {"name": "Tributary1", "coordinates": "POINT (longitude latitude)"},
         # Add more tributaries as needed
     ]

     # Convert WKT to Shapely geometry and add to the map
     for tributary in tributaries:
         geom = wkt.loads(tributary["coordinates"])
         folium.Marker([geom.y, geom.x], popup=tributary["name"]).add_to(m)

     # Save the final map
     m.save("91.html")