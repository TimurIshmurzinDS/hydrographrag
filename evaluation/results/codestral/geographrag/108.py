python
    import geopandas as gpd
    import folium
    from shapely import wkt

    # 2. Init map (Using a default location for the absence of basin data)
    m = folium.Map(location=[43.889215, 76.328361], tiles='CartoDB positron', zoom_start=8)

    # 3. Add points based on Graph Knowledge
    points = [
        {"name": "Kurty River", "wkt": "POINT(76.328361 43.889215)"},
        {"name": "Urzhar River", "wkt": "POINT(81.3315 47.1457)"}
    ]

    # 4. Draw markers
    for p in points:
        geom = wkt.loads(p["wkt"])
        folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

    m.save("108.html")