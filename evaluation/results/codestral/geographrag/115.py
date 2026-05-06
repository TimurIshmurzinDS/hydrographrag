python
    import geopandas as gpd
    import folium
    from shapely import wkt

    # 1. Load basin (Assuming we have the basin data for both rivers)
    temirlik_basin_data = gpd.read_file(r"data/temirlik_basin_data.shp").to_crs('EPSG:4326')
    byzhy_basin_data = gpd.read_file(r"data/byzhy_basin_data.shp").to_crs('EPSG:4326')

    # 2. Init map (Using the centroid of Temirlik River basin as initial location)
    centroid = temirlik_basin_data.geometry.centroid.iloc[0]
    m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=8)

    # 3. Add points based on Graph Knowledge
    points = [
        {"name": "Temirlik River", "wkt": "POINT(76.951042 43.782778)"},  # Assuming these are the correct coordinates
        {"name": "Karymsak aul", "wkt": "POINT(78.2158 44.26)"}
    ]

    # 4. Draw markers
    for p in points:
        geom = wkt.loads(p["wkt"])
        folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

    # 5. Add basins to the map
    folium.GeoJson(temirlik_basin_data.to_json(), style_function=lambda x: {'fillColor': 'blue', 'color': 'darkblue', 'fillOpacity': 0.2}).add_to(m)
    folium.GeoJson(byzhy_basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

    m.save("115.html")