python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # 1. Init map (Since basin data is not available, we'll use the coordinates of Sarkand town)
   m = folium.Map(location=[45.2436, 79.5507], tiles='CartoDB positron', zoom_start=8)

   # 2. Add points based on Graph Knowledge
   points = [
       {"name": "Sarkand town", "wkt": "POINT(79.5507 45.2436)"}
   ]

   # 3. Draw markers
   for p in points:
       geom = wkt.loads(p["wkt"])
       folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

   m.save("58.html")