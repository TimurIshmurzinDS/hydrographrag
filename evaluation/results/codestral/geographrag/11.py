python
    import geopandas as gpd
    import folium
    from shapely import wkt

    # 1. Load basin (Assuming a placeholder for this step)
    # basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')
    # centroid = basin_data.geometry.centroid.iloc[0]

    # 2. Init map (Using a placeholder location as we don't have basin data)
    m = folium.Map(location=[44.3437, 79.0553], tiles='CartoDB positron', zoom_start=8)

    # 3. Add points based on Graph Knowledge
    points = [
        {"name": "Koktal River at Araltobe village", "wkt": "POINT(79.0553 44.3437)"},
        {"name": "Plodokonzerny subsidiary farm", "wkt": "POINT(78.802213 44.6146342)"}
    ]

    # 4. Draw markers
    for p in points:
        geom = wkt.loads(p["wkt"])
        folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

    m.save("11.html")