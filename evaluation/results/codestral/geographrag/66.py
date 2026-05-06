python
    import geopandas as gpd
    import folium
    from shapely import wkt

    # 1. Load basin (Assuming we have the basin data in a shapefile)
    basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')
    centroid = basin_data.geometry.centroid.iloc[0]

    # 2. Init map
    m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=8)
    folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

    # 3. Add points based on Graph Knowledge (Assuming we have the coordinates of Temirlik village and water level measurement points)
    points = [
        {"name": "Temirlik Village", "wkt": "POINT(76.0 43.0)"},  # Replace with actual coordinates
        {"name": "Water Level Measurement Point 1", "wkt": "POINT(76.1 43.1)"},  # Replace with actual coordinates
        {"name": "Water Level Measurement Point 2", "wkt": "POINT(76.2 43.2)"}   # Replace with actual coordinates
    ]

    # 4. Draw markers
    for p in points:
        geom = wkt.loads(p["wkt"])
        folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

    m.save("66.html")