python
    import geopandas as gpd
    import folium
    from shapely import wkt

    # 1. Load basin (Assuming a basin data file is available)
    # basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')
    # centroid = basin_data.geometry.centroid.iloc[0]

    # 2. Init map (Since we don't have basin data, using average coordinates of the rivers)
    m = folium.Map(location=[43.22315, 77.20765], tiles='CartoDB positron', zoom_start=8)

    # 3. Add points based on Graph Knowledge
    points = [
        {"name": "Emel River", "wkt": "POINT(77.0401 43.2406)"},
        {"name": "Turgen River", "wkt": "POINT(77.3706 43.2057)"}
    ]

    # 4. Draw markers
    for p in points:
        geom = wkt.loads(p["wkt"])
        folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

    m.save("202.html")