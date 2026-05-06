python
         # Import necessary libraries
         import geopandas as gpd
         import pandas as pd
         import folium

         # Load temperature data for 2021 and 2022
         temp_data_2021 = pd.read_csv('temperature_data_2021.csv')
         temp_data_2022 = pd.read_csv('temperature_data_2022.csv')

         # Check for missing or anomalous data
         print(temp_data_2021.isnull().sum())
         print(temp_data_2022.isnull().sum())

         # Load river shapefile
         river = gpd.read_file('shilik_river.shp')

         # Merge temperature data with river shapefile
         merged_data_2021 = river.merge(temp_data_2021, on='location_id')
         merged_data_2022 = river.merge(temp_data_2022, on='location_id')

         # Create a folium map centered around the river
         m = folium.Map(location=[merged_data_2021['lat'].mean(), merged_data_2021['lon'].mean()], zoom_start=10)

         # Add temperature data to the map for 2021
         folium.Choropleth(
             geo_data=merged_data_2021,
             name='Temperature 2021',
             data=merged_data_2021,
             columns=['location_id', 'temperature'],
             key_on='feature.properties.location_id',
             fill_color='YlOrRd',
             fill_opacity=0.7,
             line_opacity=0.2,
             legend_name='Temperature (°C)'
         ).add_to(m)

         # Add temperature data to the map for 2022
         folium.Choropleth(
             geo_data=merged_data_2022,
             name='Temperature 2022',
             data=merged_data_2022,
             columns=['location_id', 'temperature'],
             key_on='feature.properties.location_id',
             fill_color='YlGnBu',
             fill_opacity=0.7,
             line_opacity=0.2,
             legend_name='Temperature (°C)'
         ).add_to(m)

         # Add a layer control to the map
         folium.LayerControl().add_to(m)

         # Save the map as "53.html"
         m.save("53.html")