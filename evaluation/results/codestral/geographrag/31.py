python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # 1. Load basin (Assuming we have the data for the Il River basin)
   basin_data = gpd.read_file(r"data/il_river_basin.shp").to_crs('EPSG:4326')
   centroid = basin_data.geometry.centroid.iloc[0]

   # 2. Init map
   m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=8)
   folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'blue', 'color': 'darkblue', 'fillOpacity': 0.2}).add_to(m)

   # 3. Since we don't have specific data points for water consumption, no additional points are added here.

   m.save("il_river_basin.html")