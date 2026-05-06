python
        import geopandas as gpd
        import folium
        # Load data
        drainage_network = gpd.read_file('drainage_network.shp')
        # Calculate length of each water object
        drainage_network['length'] = drainage_network.geometry.length
        # Calculate area of the basin
        basin_area = drainage_network.unary_union.convex_hull.area
        # Calculate density
        drainage_density = drainage_network['length'].sum() / basin_area
        print('Drainage density:', drainage_density)
        # Visualize results on a map
        m = folium.Map(location=[drainage_network.geometry.centroid.y.mean(), drainage_network.geometry.centroid.x.mean()], zoom_start=10)
        folium.GeoJson(drainage_network).add_to(m)
        m.save('172.html')