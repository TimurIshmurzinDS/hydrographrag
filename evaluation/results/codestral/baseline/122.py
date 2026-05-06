python
         import pandas as pd
         import folium

         # Load the data
         data = pd.read_csv('kishi_almaty_river_data.csv')

         # Find the peak water level
         peak_water_level = data['Water Level'].max()

         # Calculate the mean water level
         mean_water_level = data['Water Level'].mean()

         # Compare the peak water level with the mean water level
         difference = peak_water_level - mean_water_level

         print(f'Peak Water Level: {peak_water_level}')
         print(f'Mean Water Level: {mean_water_level}')
         print(f'Difference: {difference}')

         # Visualize on a map using folium
         m = folium.Map(location=[43.2567, 76.9286], zoom_start=10)
         folium.Marker([43.2567, 76.9286], popup=f'Peak Water Level: {peak_water_level}\nMean Water Level: {mean_water_level}').add_to(m)
         m.save("122.html")