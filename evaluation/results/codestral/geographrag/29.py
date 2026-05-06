python
    import geopandas as gpd
    import folium
    from shapely import wkt

    # 1. Load basin (Assuming a placeholder for basin data)
    # basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')
    # centroid = basin_data.geometry.centroid.iloc[0]

    # 2. Init map (Using approximate coordinates for Almaty City as no specific basin data is provided)
    m = folium.Map(location=[43.25, 76.9], tiles='CartoDB positron', zoom_start=8)

    # 3. Add points based on Graph Knowledge
    points = [
        {"name": "Uzyn Kargaly River at Fabrichny settlement", "wkt": "POINT(76.25 43.1)"}
    ]

    # 4. Draw markers
    for p in points:
        geom = wkt.loads(p["wkt"])
        folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

    m.save("29.html")