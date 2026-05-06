python
         import pandas as pd
         from sklearn.linear_model import LinearRegression
         import folium

         # Load data
         gravity_data = pd.read_csv('jupiter_gravity_data.csv')
         mass_data = pd.read_csv('jupiter_mass_data.csv')
         velocity_data = pd.read_csv('jupiter_velocity_data.csv')
         river_level_data = pd.read_csv('baskan_river_level_data.csv')

         # Merge data into a single DataFrame
         df = pd.concat([gravity_data, mass_data, velocity_data, river_level_data], axis=1)

         # Create and train the model
         X = df[['jupiter_gravity', 'jupiter_mass', 'jupiter_velocity']]
         y = df['river_level']
         model = LinearRegression()
         model.fit(X, y)

         # Predict river level for the last data point
         last_data_point = df[['jupiter_gravity', 'jupiter_mass', 'jupiter_velocity']].iloc[-1]
         predicted_river_level = model.predict([last_data_point])

         # Visualize on a map using folium
         m = folium.Map(location=[39.8675, 40.279], zoom_start=10)
         folium.Marker(
             location=[39.8675, 40.279],
             popup='Predicted River Level: {}'.format(predicted_river_level[0]),
             icon=folium.Icon(color='blue')
         ).add_to(m)

         # Save the map
         m.save("218.html")