python
        import geopandas as gpd
        import folium

        # Load data
        kurty_river = gpd.read_file('kurty_river.shp')
        lepsy_river = gpd.read_file('lepsy_river.shp')

        # Define agricultural water demand (in cubic meters)
        agricultural_demand = 1000000000  # Example value, replace with actual data

        # Calculate total water volume from both rivers
        total_water_volume = kurty_river['water_volume'].sum() + lepsy_river['water_volume'].sum()

        # Check if there is enough water for agricultural demand
        if total_water_volume >= agricultural_demand:
            print("There is enough water from Kurty River and Lepsy River to meet the agricultural demand.")
        else:
            print("There is not enough water from Kurty River and Lepsy River to meet the agricultural demand.")

        # Visualize results on a map using folium
        m = folium.Map(location=[kurty_river['geometry'].centroid.y.mean(), kurty_river['geometry'].centroid.x.mean()], zoom_start=10)

        folium.GeoJson(kurty_river, name='Kurty River').add_to(m)
        folium.GeoJson(lepsy_river, name='Lepsy River').add_to(m)

        folium.LayerControl().add_to(m)

        m.save("120.html")