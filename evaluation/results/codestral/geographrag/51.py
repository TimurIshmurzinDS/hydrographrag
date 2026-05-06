python
    import geopandas as gpd
    import folium
    from shapely import wkt

    # 1. Load basin (Assuming a placeholder for basin data)
    basin_data = None

    # 2. Init map (Since we don't have basin data, using default coordinates)
    m = folium.Map(location=[43.889215, 76.328361], tiles='CartoDB positron', zoom_start=8)

    # 3. Add points based on Graph Knowledge
    points = [
        {"name": "Kurty River (January)", "wkt": "POINT(76.328361 43.889215)"},
        {"name": "Kurty River (February)", "wkt": "POINT(76.328361 43.889215)"}
    ]

    # 4. Draw markers
    for p in points:
        geom = wkt.loads(p["wkt"])
        folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

    m.save("51.html")