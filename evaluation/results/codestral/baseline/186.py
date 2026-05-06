python
        import pandas as pd
        import geopandas as gpd
        from sklearn.linear_model import LinearRegression
        import folium
        from folium.plugins import HeatMap

        # Load data
        pollution_data = pd.read_csv('pollution_data.csv')
        water_quality_data = pd.read_csv('water_quality_data.csv')

        # Convert to GeoDataFrame
        gdf_pollution = gpd.GeoDataFrame(pollution_data, geometry=gpd.points_from_xy(pollution_data.longitude, pollution_data.latitude))
        gdf_water_quality = gpd.GeoDataFrame(water_quality_data, geometry=gpd.points_from_xy(water_quality_data.longitude, water_quality_data.latitude))

        # Spatial analysis (e.g., interpolation) to estimate pollution spread and its impact on water quality
        # ...

        # Statistical analysis (e.g., correlation or regression) to determine the relationship between river pollution and water quality used in agriculture
        X = gdf_pollution['pollution_level'].values.reshape(-1, 1)
        Y = gdf_water_quality['water_quality_index'].values.reshape(-1, 1)
        model = LinearRegression().fit(X, Y)

        # Visualization
        m = folium.Map([gdf_pollution.geometry.y.mean(), gdf_pollution.geometry.x.mean()], zoom_start=10)

        # Add pollution heatmap
        HeatMap(data=gdf_pollution[['latitude', 'longitude', 'pollution_level']].values.tolist(), radius=15).add_to(m)

        # Add water quality points with color based on the predicted water quality index
        for idx, row in gdf_water_quality.iterrows():
            folium.CircleMarker([row['latitude'], row['longitude']], radius=5, color='blue', fill=True, fill_color='blue' if model.predict([[row['pollution_level']]])[0][0] > threshold else 'green').add_to(m)

        m.save("186.html")