python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the basin data
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium map
   m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron')

   # Add the basin to the map
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries for river coordinates and water level data (replace with actual data)
   rivers = [
       {"name": "Karatal River", "water_level": 150, "date": "2023-04-01"},
       {"name": "Koktal River", "water_level": 160, "date": "2023-04-01"}
   ]

   # Normal water level threshold (replace with actual value)
   normal_water_level = 155

   for river in rivers:
       if river["water_level"] < normal_water_level:
           status = "Неработоспособен"
       else:
           status = "Работоспособен"

       folium.Marker(location=[0, 0], popup=f"{river['name']}: {status}").add_to(m)

   # Save the final map
   m.save("143.html")