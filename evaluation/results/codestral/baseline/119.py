python
         import pandas as pd
         import folium
         from scipy import stats
         # Load data
         byzhy_data = pd.read_csv('byzhy_river.csv')
         tekeli_data = pd.read_csv('tekeli_river.csv')
         # Data cleaning and preprocessing
         byzhy_data = byzhy_data.dropna()
         tekeli_data = tekeli_data.dropna()
         # Select relevant indicators for comparison
         indicators = ['ph', 'pollutants', 'biodiversity']
         # Statistical analysis
         byzhy_stats = byzhy_data[indicators].describe()
         tekeli_stats = tekeli_data[indicators].describe()
         print('Byzhy River statistics:')
         print(byzhy_stats)
         print('Tekeli River statistics:')
         print(tekeli_stats)
         # Visualization on map
         m = folium.Map(location=[55, 37], zoom_start=6)
         byzhy_layer = folium.FeatureGroup(name='Byzhy River')
         tekeli_layer = folium.FeatureGroup(name='Tekeli River')
         for i, row in byzhy_data.iterrows():
             byzhy_layer.add_child(folium.CircleMarker(location=[row['lat'], row['lon']], radius=5, color='blue', fill_color='blue'))
         for i, row in tekeli_data.iterrows():
             tekeli_layer.add_child(folium.CircleMarker(location=[row['lat'], row['lon']], radius=5, color='red', fill_color='red'))
         m.add_child(byzhy_layer)
         m.add_child(tekeli_layer)
         folium.LayerControl().add_to(m)
         m.save('119.html')