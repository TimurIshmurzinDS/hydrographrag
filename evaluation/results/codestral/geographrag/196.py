python
    import geopandas as gpd
    import folium
    from shapely import wkt

    # 2. Init map (Using an approximate center point for the map initialization)
    m = folium.Map(location=[43.8, 76.5], tiles='CartoDB positron', zoom_start=8)

    # 3. Add points based on Graph Knowledge
    points = [
        {"name": "Emel River", "wkt": "POINT(77.0401 43.2406)"},
        {"name": "Koksu River", "wkt": "POINT(78.5517 44.3940)"}
    ]

    # 4. Draw markers
    for p in points:
        geom = wkt.loads(p["wkt"])
        folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

    m.save("196.html")