python
         import pandas as pd
         import folium

         # Load inflation data
         inflation_data = pd.read_csv('inflation_data.csv')

         # Load Sharyn River coordinates data
         river_data = pd.read_csv('river_coordinates.csv')

         # Merge two datasets based on geographical coordinates
         merged_data = pd.merge(inflation_data, river_data, on='coordinates')

         # Create a map centered around the Sharyn River
         m = folium.Map(location=[merged_data['latitude'].mean(), merged_data['longitude'].mean()], zoom_start=10)

         # Add inflation data to the map using color scale
         for i in range(len(merged_data)):
             folium.CircleMarker(location=[merged_data.iloc[i]['latitude'], merged_data.iloc[i]['longitude']],
                                 radius=5,
                                 color='red',
                                 fill=True,
                                 fill_color='red' if merged_data.iloc[i]['inflation_rate'] > 0 else 'green',
                                 fill_opacity=0.6).add_to(m)

         # Save the map as "272.html"
         m.save("272.html")