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

       # Hardcoded list of dictionaries for rivers and observation points
       features = [
           {"name": "Tentek River", "coordinates": wkt.loads("POINT (37.618945 55.752004)")},
           {"name": "Tekes River", "coordinates": wkt.loads("POINT (37.629872 55.743751)")},
           {"name": "Observation Point", "coordinates": wkt.loads("POINT (37.620872 55.748751)")}
       ]

       # Add rivers and observation point to the map
       for feature in features:
           folium.Marker(location=[feature["coordinates"].y, feature["coordinates"].x], popup=feature["name"]).add_to(m)

       # Save the final map
       m.save("242.html")