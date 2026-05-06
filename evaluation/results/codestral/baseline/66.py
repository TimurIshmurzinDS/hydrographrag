python
         import folium
         from folium.plugins import MarkerCluster
         import pandas as pd

         # Load the data
         equipment_data = pd.read_csv('equipment_data.csv')  # Replace with your actual file path

         # Create a base map
         m = folium.Map(location=[42.358056, 71.401944], zoom_start=10)  # Coordinates for Temirlik River

         # Create a marker cluster object
         marker_cluster = MarkerCluster().add_to(m)

         # Add equipment data to the map
         for i in range(len(equipment_data)):
             folium.Marker(
                 location=[equipment_data.iloc[i]['Latitude'], equipment_data.iloc[i]['Longitude']],
                 popup=f"Equipment ID: {equipment_data.iloc[i]['ID']}<br>Status: {equipment_data.iloc[i]['Status']}",
                 icon=folium.Icon(color='green' if equipment_data.iloc[i]['Status'] == 'Working' else 'red')
             ).add_to(marker_cluster)

         # Save the map
         m.save("66.html")