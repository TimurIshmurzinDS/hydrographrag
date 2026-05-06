python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the basin data
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium map
   m = folium.Map(location=[basin.centroid.y.mean(), basin.centroid.x.mean()], tiles='CartoDB positron')

   # Add the basin to the map
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries for water level data (replace with actual data)
   water_level_data = [
       {"river": "Koktal River", "water_level": Water_level_Valuecm, "date": Date_water_level_Value},
       # Add more data as needed
   ]

   # Print the list of posts on Koktal River and their current water level
   for post in water_level_data:
       if post["river"] == "Koktal River":
           print(f"River: {post['river']}, Water Level: {post['water_level']} cm, Date: {post['date']}")

   # Save the final map
   m.save("88.html")