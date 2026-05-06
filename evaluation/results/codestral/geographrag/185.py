python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # 1. Load basin (assuming a shape file for the river Byszh is available)
   basin_data = gpd.read_file(r"data/byszh_basin.shp").to_crs('EPSG:4326')
   centroid = basin_data.geometry.centroid.iloc[0]

   # 2. Init map
   m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=8)
   folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'blue', 'color': 'darkblue', 'fillOpacity': 0.2}).add_to(m)

   # 3. Add points for water intake and crop yield data (assuming WKT coordinates are available)
   points = [
       {"name": "Water Intake", "wkt": "POINT(76.0 43.0)"},  # Replace with actual coordinates
       {"name": "Crop Yield Area 1", "wkt": "POINT(76.2 43.2)"},  # Replace with actual coordinates
       {"name": "Crop Yield Area 2", "wkt": "POINT(75.8 42.9)"}   # Replace with actual coordinates
   ]

   # 4. Draw markers
   for p in points:
       geom = wkt.loads(p["wkt"])
       folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

   m.save("185.html")