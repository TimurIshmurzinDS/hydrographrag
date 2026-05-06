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

   # Hardcoded list of dictionaries containing water consumption data for the rivers
   water_consumption = [
       {"river": "Tekes River", "values": [10, 12, 15, 13, 14]},
       {"river": "Bayankol River", "values": [8, 9, 11, 10, 10]}
   ]

   # Calculate the average water consumption for each river over the last 5 years
   avg_consumption = {item["river"]: sum(item["values"]) / len(item["values"]) for item in water_consumption}

   # Current water consumption values (assuming these are available)
   current_consumption = {"Tekes River": 16, "Bayankol River": 12}

   # Calculate the increase in water consumption compared to the average
   increase = {river: current_consumption[river] - avg for river, avg in avg_consumption.items()}

   # Find the river with the largest increase in water consumption
   max_increase_river = max(increase, key=increase.get)

   print(f"The river that showed the largest increase in water flow compared to its average value over the last 5 years is {max_increase_river}.")

   # Save the final map
   m.save("125.html")