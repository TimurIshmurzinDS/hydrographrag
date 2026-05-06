python
         import folium
         import pandas as pd
         # Load water quality data
         data = pd.read_csv('water_quality_data.csv')
         # Define coordinates of Emel River and its tributaries
         emel_coords = [(54.9836, 72.0167), (54.9786, 72.0217)]
         tributary_coords = [(54.9786, 72.0217), (54.9736, 72.0267)]
         # Create a map centered around Emel River
         m = folium.Map(location=[54.9836, 72.0167], zoom_start=12)
         # Add Emel River to the map
         folium.PolyLine(emel_coords, color="blue", weight=2.5, opacity=1).add_to(m)
         # Add tributaries to the map
         folium.PolyLine(tributary_coords, color="green", weight=2.5, opacity=1).add_to(m)
         # Add water quality data points to the map
         for i in range(len(data)):
             if data['location'][i] == 'Emel River':
                 folium.CircleMarker(location=[data['latitude'][i], data['longitude'][i]], radius=5, color='blue', fill_color='blue').add_to(m)
             else:
                 folium.CircleMarker(location=[data['latitude'][i], data['longitude'][i]], radius=5, color='green', fill_color='green').add_to(m)
         # Save the map as an HTML file
         m.save("265.html")