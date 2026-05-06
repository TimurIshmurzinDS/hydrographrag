python
        import geopandas as gpd
        from shapely.geometry import LineString
        import folium

        # Load data
        rivers = gpd.read_file('rivers.geojson')  # replace with your file path

        # Create topology
        rivers['geometry'] = rivers['geometry'].apply(lambda geom: LineString(geom.coords))
        rivers['start'] = rivers['geometry'].apply(lambda geom: geom.coords[0])
        rivers['end'] = rivers['geometry'].apply(lambda geom: geom.coords[-1])

        # Check if Емель is a tributary of Каратал
        emel = rivers[rivers['name'] == 'Емель']['geometry'].iloc[0]
        karatal = rivers[rivers['name'] == 'Каратал']['geometry'].iloc[0]

        if emel.intersects(karatal):
            # Calculate length of the section
            section_length = emel.intersection(karatal).length
            print(f'The length of the section is {section_length} meters')

            # Visualize on map
            m = folium.Map(location=[54, 60], zoom_start=10)
            folium.GeoJson(rivers).add_to(m)
            folium.GeoJson(emel.intersection(karatal), style_function=lambda x: {'color': 'red'}).add_to(m)
            m.save("97.html")
        else:
            print('Емель is not a tributary of Каратал')