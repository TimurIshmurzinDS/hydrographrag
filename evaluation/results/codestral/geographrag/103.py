python
        import geopandas as gpd
        import folium
        from shapely import wkt

        # 1. Load basin (assuming a basin data file is available)
        basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')
        centroid = basin_data.geometry.centroid.iloc[0]

        # 2. Init map
        m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=8)
        folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

        # 3. Add points based on Graph Knowledge
        points = [
            {"name": "Urzhar River", "wkt": "POINT(81.3315 47.1457)"},
            {"name": "Dos River (Aynabulak railway station)", "wkt": "POINT(77.994303 44.623949)"},
            {"name": "Karatal River (Akzhar aul)", "wkt": "POINT(80.3849 45.4753)"},
            {"name": "Karatal River (Ushtobe town)", "wkt": "POINT(77.5843 45.1532)"}
        ]

        # 4. Draw markers
        for p in points:
            geom = wkt.loads(p["wkt"])
            folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

        m.save("103.html")