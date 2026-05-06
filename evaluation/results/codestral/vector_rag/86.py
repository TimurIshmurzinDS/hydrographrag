python
       import geopandas as gpd
       import folium
       from shapely import wkt

       # Load the shapefile and convert to CRS 'EPSG:4326'
       basin = gpd.read_file(r"data/basin_data.shp")
       basin = basin.to_crs('EPSG:4326')

       # Initialize folium map using the centroid of the shapefile
       m = folium.Map(location=[basin.geometry.centroid.y.mean(), basin.geometry.centroid.x.mean()], tiles='CartoDB positron')

       # Add the basin to the map
       folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

       # Hardcoded list of dictionaries for rivers (replace with actual data if available)
       rivers = [{'name': 'Temirlik River'}, {'name': 'Turgen River'}, {'name': 'Karaoy River'}]

       # Add rivers to the map (for visualization purposes, no specific coordinates provided)
       for river in rivers:
           folium.Marker(location=[0, 0], popup=river['name']).add_to(m)

       # Save the final map
       m.save("86.html")