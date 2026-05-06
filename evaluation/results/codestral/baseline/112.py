python
        import geopandas as gpd
        import rasterio
        from rasterstats import zonal_stats
        import folium

        # Load river data
        rivers = gpd.read_file('rivers.geojson')

        # Load water consumption data
        with rasterio.open('water_consumption.tif') as src:
            water_consumption = src.read(1)
            transform = src.transform

        # Calculate water consumption for each river
        stats = zonal_stats(rivers, water_consumption, affine=transform, stats="mean")
        rivers['water_consumption'] = [stat['mean'] for stat in stats]

        # Filter the data for the specified rivers
        selected_rivers = rivers[rivers['name'].isin(['Kurty River', 'Urzhar River', 'Byzhy River'])]

        # Create a map centered around the selected rivers
        m = folium.Map(location=[selected_rivers['geometry'].centroid.y.mean(), selected_rivers['geometry'].centroid.x.mean()], zoom_start=10)

        # Add rivers to the map with water consumption as popup
        for _, r in selected_rivers.iterrows():
            folium.GeoJson(r['geometry'], style_function=lambda x: {'color': 'blue'}, tooltip=f"{r['name']}: {r['water_consumption']}").add_to(m)

        # Save the map as HTML
        m.save("112.html")