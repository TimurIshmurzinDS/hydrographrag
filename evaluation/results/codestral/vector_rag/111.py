python
       import geopandas as gpd
       import folium
       from shapely import wkt

       # Load the shapefile and convert to CRS 'EPSG:4326'
       basin = gpd.read_file(r"data/basin_data.shp")
       basin = basin.to_crs('EPSG:4326')

       # Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
       m = folium.Map(location=[basin.geometry.centroid.y, basin.geometry.centroid.x], tiles='CartoDB positron')

       # Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
       folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

       # Hardcoded list of dictionaries with river and village coordinates (WKT)
       entities = [
           {"name": "Temirlik River", "coordinates": "POINT (71.345678 42.901234)"},
           {"name": "Aksu River", "coordinates": "POINT (71.567890 42.789012)"},
           {"name": "Temirlik village", "coordinates": "POINT (71.356789 42.801234)"}
       ]

       # Add rivers and village to the map
       for entity in entities:
           point = wkt.loads(entity["coordinates"])
           folium.Marker([point.y, point.x], popup=entity["name"]).add_to(m)

       # Save the final map
       m.save("111.html")