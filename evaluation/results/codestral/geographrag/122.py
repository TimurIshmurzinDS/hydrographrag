python
    import geopandas as gpd
    import folium
    from shapely import wkt

    # 1. Load basin (Assuming a default centroid for Almaty City)
    centroid = [43.25, 76.90]

    # 2. Init map
    m = folium.Map(location=centroid, tiles='CartoDB positron', zoom_start=8)

    # 3. Add points based on Graph Knowledge
    points = [
        {"name": "M Mynzhilky", "wkt": "POINT(76.54 43.15)"},
        {"name": "Tuyuksu Alpine base", "wkt": "POINT(77.078147 43.084405)"},
        {"name": "(near Almaty)", "wkt": "POINT(77.0331 43.0927)"}
    ]

    # 4. Draw markers
    for p in points:
        geom = wkt.loads(p["wkt"])
        folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

    m.save("122.html")