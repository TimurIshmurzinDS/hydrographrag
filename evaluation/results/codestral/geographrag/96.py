python
    import geopandas as gpd
    import folium
    from shapely import wkt

    # 1. Load basin (Assuming we have a basin data file, but it's not provided in the graph knowledge)
    # basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')
    # centroid = basin_data.geometry.centroid.iloc[0]

    # 2. Init map (Since we don't have a basin data file, we will use the average of the two points as the center)
    m = folium.Map(location=[45.984323, 79.663027], tiles='CartoDB positron', zoom_start=8)

    # 3. Add points based on Graph Knowledge
    points = [
        {"name": "Urzhar River", "wkt": "POINT(81.3315 47.1457)"},
        {"name": "Dos River", "wkt": "POINT(77.994303 44.623949)"}
    ]

    # 4. Draw markers
    for p in points:
        geom = wkt.loads(p["wkt"])
        folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

    m.save("96.html")