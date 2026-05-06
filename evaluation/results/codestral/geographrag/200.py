python
    import geopandas as gpd
    import folium
    from shapely import wkt

    # 1. Load basin (Assuming a placeholder for basin data)
    basin_data = None

    # If basin data is available, uncomment and use the following lines:
    # basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')
    # centroid = basin_data.geometry.centroid.iloc[0]

    # 2. Init map (Using a default location as no basin data is provided)
    m = folium.Map(location=[43.9318, 79.6890], tiles='CartoDB positron', zoom_start=8)

    # If basin data is available, uncomment and use the following line to add it to the map:
    # folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

    # 3. Add points based on Graph Knowledge
    points = [
        {"name": "Kishi Osek River", "wkt": "POINT(79.689005 43.9318)"}
    ]

    # 4. Draw markers
    for p in points:
        geom = wkt.loads(p["wkt"])
        folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

    m.save("200.html")