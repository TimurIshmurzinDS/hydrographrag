python
        from osgeo import ogr
        import folium

        # Load data
        driver = ogr.GetDriverByName('ESRI Shapefile')
        dataSource = driver.Open('/path/to/rivers_data.shp', 0)
        layer = dataSource.GetLayer()

        # Find coordinates of the headwaters for Tenteck and Byzh rivers
        tenteck_coords, byzh_coords = None, None
        for feature in layer:
            if feature.GetField('river') == 'Tenteck':
                geometry = feature.GetGeometryRef()
                points = geometry.GetPoints()
                tenteck_coords = max(points, key=lambda point: point[1])
            elif feature.GetField('river') == 'Byzh':
                geometry = feature.GetGeometryRef()
                points = geometry.GetPoints()
                byzh_coords = max(points, key=lambda point: point[1])

        # Compare coordinates
        print("Tenteck headwaters coordinates:", tenteck_coords)
        print("Byzh headwaters coordinates:", byzh_coords)

        # Visualize on a map
        m = folium.Map(location=[55, 37], zoom_start=4)
        folium.Marker(tenteck_coords[::-1], popup='Tenteck headwaters').add_to(m)
        folium.Marker(byzh_coords[::-1], popup='Byzh headwaters').add_to(m)
        m.save("94.html")