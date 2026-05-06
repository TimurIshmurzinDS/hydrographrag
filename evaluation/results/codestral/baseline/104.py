python
        import geopandas as gpd
        from shapely.geometry import Point
        from shapely.ops import nearest_points
        import folium

        # Load data
        rivers = gpd.read_file('rivers.geojson')  # replace with your file path

        # Check if Shyzhyn is a tributary of Dos
        shyzhyn = rivers[rivers['name'] == 'Shyzhyn'].geometry.values[0]
        dos = rivers[rivers['name'] == 'Dos'].geometry.values[0]

        if shyzhyn.intersects(dos):
            print("Shyzhyn is a tributary of Dos.")
        else:
            print("Shyzhyn is not a tributary of Dos.")
            exit()

        # Find the merging point
        intersection = shyzhyn.intersection(dos)

        # Calculate distance to the merging point from the start of Shyzhyn
        start_shyzhyn = Point(shyzhyn.coords[0])
        nearest_geom, _ = nearest_points(start_shyzhyn, intersection)
        distance = start_shyzhyn.distance(nearest_geom)

        print("Distance to the merging point: ", distance)

        # Visualize on map
        m = folium.Map(location=[54.8, 69.1], zoom_start=7)

        folium.GeoJson(shyzhyn).add_to(m)
        folium.GeoJson(dos).add_to(m)
        folium.Marker([intersection.y, intersection.x]).add_to(m)

        m.save("104.html")