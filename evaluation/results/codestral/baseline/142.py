python
         import folium
         import pandas as pd
         # Assuming you have a CSV file 'monitoring_equipment.csv' with columns 'lat', 'lon', and 'status'
         data = pd.read_csv('monitoring_equipment.csv')
         m = folium.Map(location=[data['lat'].mean(), data['lon'].mean()], zoom_start=10)
         for i, row in data.iterrows():
             if row['status'] == 'working':
                 color = 'green'
             else:
                 color = 'red'
             folium.CircleMarker(location=[row['lat'], row['lon']], radius=5, color=color, fill_color=color).add_to(m)
         m.save("142.html")