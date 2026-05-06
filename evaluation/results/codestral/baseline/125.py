python
         import pandas as pd
         import folium
         # Load data
         tekes_data = pd.read_csv('tekes_river_flow.csv')
         bayankol_data = pd.read_csv('bayankol_river_flow.csv')
         # Calculate mean flow for each river
         tekes_mean = tekes_data['flow'].mean()
         bayankol_mean = bayankol_data['flow'].mean()
         # Calculate difference from mean for each year
         tekes_data['diff'] = tekes_data['flow'] - tekes_mean
         bayankol_data['diff'] = bayankol_data['flow'] - bayankol_mean
         # Find the year with maximum increase in flow above mean
         max_tekes_year = tekes_data.loc[tekes_data['diff'].idxmax(), 'year']
         max_bayankol_year = bayankol_data.loc[bayankol_data['diff'].idxmax(), 'diff']
         # Determine which river had the greatest increase in flow above mean
         if tekes_data.loc[tekes_data['year'] == max_tekes_year, 'diff'].values > bayankol_data.loc[bayankol_data['year'] == max_bayankol_year, 'diff'].values:
             print('Tekes River had the greatest increase in flow above mean')
         else:
             print('Bayankol River had the greatest increase in flow above mean')
         # Visualize on map (assuming coordinates are available)
         m = folium.Map(location=[55, 100], zoom_start=4)
         folium.Marker([tekes_data['lat'].mean(), tekes_data['lon'].mean()], popup='Tekes River').add_to(m)
         folium.Marker([bayankol_data['lat'].mean(), bayankol_data['lon'].mean()], popup='Bayankol River').add_to(m)
         m.save("125.html")