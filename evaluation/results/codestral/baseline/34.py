python
        import pandas as pd
        import geopandas as gpd
        import folium

        # Load pollution data
        pollution_data = pd.read_csv('pollution_data.csv')

        # Load river geometry data
        river_geometry = gpd.read_file('river_geometry.geojson')

        # Merge data on a common identifier
        merged_data = river_geometry.merge(pollution_data, on='id')

        # Create a map centered around the river
        m = folium.Map(location=[merged_data['lat'].mean(), merged_data['lon'].mean()], zoom_start=10)

        # Add pollution data to the map
        folium.Choropleth(
            geo_data=merged_data,
            name='Pollution',
            data=merged_data,
            columns=['id', 'pollution_index'],
            key_on='feature.properties.id',
            fill_color='YlOrRd',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Pollution Index'
        ).add_to(m)

        # Save the map as an HTML file
        m.save("34.html")