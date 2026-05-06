python
         import pandas as pd
         import folium

         # Load data
         data = pd.read_csv('karkara_river_data.csv')

         # Split data into two decades
         last_decade = data[data['year'] >= 2010]
         previous_decade = data[data['year'] < 2010]

         # Calculate average water consumption for each decade
         avg_last_decade = last_decade['water_consumption'].mean()
         avg_previous_decade = previous_decade['water_consumption'].mean()

         # Calculate difference
         diff = avg_last_decade - avg_previous_decade
         print(f'Difference in water consumption: {diff}')

         # Visualize data on a map
         m = folium.Map(location=[data['lat'].mean(), data['lon'].mean()], zoom_start=10)

         for index, row in last_decade.iterrows():
             folium.CircleMarker([row['lat'], row['lon']], radius=5, color='blue').add_to(m)

         for index, row in previous_decade.iterrows():
             folium.CircleMarker([row['lat'], row['lon']], radius=5, color='red').add_to(m)

         m.save("54.html")