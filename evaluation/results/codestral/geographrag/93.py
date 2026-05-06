python
      import geopandas as gpd
      import folium
      from shapely import wkt

      # 1. Load basin (Assuming a placeholder for basin data)
      basin_data = None

      # 2. Init map with default coordinates since basin data is not available
      m = folium.Map(location=[45.4753, 80.3849], tiles='CartoDB positron', zoom_start=8)

      # 3. Add points based on Graph Knowledge
      points = [
          {"name": "Karatal River", "wkt": "POINT(80.3849 45.4753)"},
          {"name": "Akzhar aul", "wkt": "POINT(80.3849 45.4753)"},
          {"name": "Ushtobe town", "wkt": "POINT(77.5843 45.1532)"}
      ]

      # 4. Draw markers
      for p in points:
          geom = wkt.loads(p["wkt"])
          folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

      m.save("93.html")