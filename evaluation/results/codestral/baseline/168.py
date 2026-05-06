python
        import geopandas as gpd
        import folium
        # Load data
        emel = gpd.read_file('emel.shp')
        sarykan = gpd.read_file('sarykan.shp')
        # Add basin column
        emel['basin'] = 'Emel'
        sarykan['basin'] = 'Sarykan'
        # Merge data
        rivers = pd.concat([emel, sarykan])
        # Calculate topological connectivity
        connected = gpd.sjoin(rivers[rivers['basin'] == 'Emel'], rivers[rivers['basin'] == 'Sarykan'], how='inner', op='intersects')
        # Visualize results on map
        m = folium.Map(location=[54, 60], zoom_start=7)
        folium.GeoJson(rivers).add_to(m)
        for i, row in connected.iterrows():
            folium.PolyLine([row['geometry'].coords[0], row['geometry'].coords[-1]], color='red').add_to(m)
        m.save("168.html")