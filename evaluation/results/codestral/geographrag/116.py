python
    import geopandas as gpd
    import folium
    from shapely import wkt

    # 1. Load basin (Assuming we have a basin data file, but it's not provided in the graph knowledge)
    # basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')
    # centroid = basin_data.geometry.centroid.iloc[0]

    # 2. Init map (Since we don't have basin data, we'll use average coordinates of the rivers as a center)
    m = folium.Map(location=[45.32765, 78.50975], tiles='CartoDB positron', zoom_start=8)

    # 3. Add points based on Graph Knowledge
    points = [
        {"name": "Tekeli River", "wkt": "POINT(78.4551 44.5147)"},
        {"name": "Lepsy River", "wkt": "POINT(78.5644 46.1406)"}
    ]

    # 4. Draw markers
    for p in points:
        geom = wkt.loads(p["wkt"])
        folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

    m.save("116.html")