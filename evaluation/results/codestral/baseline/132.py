python
         import pandas as pd
         import folium
         # Load data
         lepsy_data = pd.read_csv('lepsy_river_data.csv')
         tekkes_data = pd.read_csv('tekkes_river_data.csv')
         # Find year with highest discharge for each river
         max_discharge_lepsy = lepsy_data['Discharge'].max()
         year_max_discharge_lepsy = lepsy_data[lepsy_data['Discharge'] == max_discharge_lepsy]['Year'].values[0]
         max_discharge_tekkes = tekkes_data['Discharge'].max()
         year_max_discharge_tekkes = tekkes_data[tekkes_data['Discharge'] == max_discharge_tekkes]['Year'].values[0]
         # Compare years
         if year_max_discharge_lepsy > year_max_discharge_tekkes:
             print(f'The Lepsy River had the highest discharge in {year_max_discharge_lepsy}, which is later than {year_max_discharge_tekkes} for Tekes River.')
         elif year_max_discharge_lepsy < year_max_discharge_tekkes:
             print(f'The Tekes River had the highest discharge in {year_max_discharge_tekkes}, which is later than {year_max_discharge_lepsy} for Lepsy River.')
         else:
             print(f'Both rivers had their highest discharge in {year_max_discharge_lepsy}.')
         # Visualization (assuming coordinates are available)
         m = folium.Map()
         folium.Marker([lepsy_data['Latitude'].mean(), lepsy_data['Longitude'].mean()], popup='Lepsy River').add_to(m)
         folium.Marker([tekkes_data['Latitude'].mean(), tekkes_data['Longitude'].mean()], popup='Tekes River').add_to(m)
         m.save("132.html")