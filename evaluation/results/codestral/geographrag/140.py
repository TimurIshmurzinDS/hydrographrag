python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # 1. Load basin (Assuming a basin shape file is available)
   basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')
   centroid = basin_data.geometry.centroid.iloc[0]

   # 2. Init map
   m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=8)
   folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # 3. Add sensor points based on available data
   points = [
       {"name": "Токыраун Sensor", "wkt": "POINT(76.0 43.0)"},  # Replace with actual coordinates
       {"name": "Аягоз Sensor", "wkt": "POINT(75.0 42.0)"}    # Replace with actual coordinates
   ]

   # 4. Draw markers
   for p in points:
       geom = wkt.loads(p["wkt"])
       folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

   m.save("140.html")