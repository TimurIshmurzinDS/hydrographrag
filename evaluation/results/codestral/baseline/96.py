python
        import geopandas as gpd
        from shapely.geometry import Point
        from shapely.ops import nearest_points
        from shapely.ops import unary_union
        import folium

        # Load data
        rivers = gpd.read_file('rivers.shp')  # replace with your file path

        # Filter data for Uzhar and Dos rivers
        uzhar = rivers[rivers['name'] == 'Uzhar'].iloc[0]
        dos = rivers[rivers['name'] == 'Dos'].iloc[0]

        # Find hydrographic points (start and end of the river)
        uzhar_start = Point(uzhar.geometry.coords[0])
        uzhar_end = Point(uzhar.geometry.coords[-1])
        dos_start = Point(dos.geometry.coords[0])
        dos_end = Point(dos.geometry.coords[-1])

        # Find the nearest points between Uzhar and Dos rivers
        uzhar_point, dos_point = nearest_points(uzhar.geometry, dos.geometry)

        # Calculate distance
        distance = uzhar_point.distance(dos_point)
        print(f'The distance between Uzhar and Dos rivers is: {distance} meters')

        # Visualization on a map
        m = folium.Map(location=[uzhar_start.y, uzhar_start.x], zoom_start=6)

        # Add markers for hydrographic points
        folium.Marker([uzhar_point.y, uzhar_point.x], popup='Uzhar').add_to(m)
        folium.Marker([dos_point.y, dos_point.x], popup='Dos').add_to(m)

        # Add line between the points
        folium.PolyLine([(uzhar_point.y, uzhar_point.x), (dos_point.y, dos_point.x)]).add_to(m)

        m.save("96.html")