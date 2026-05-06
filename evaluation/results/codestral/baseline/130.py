python
         import pandas as pd
         from statsmodels.tsa.stattools import adfuller
         import folium
         # Load data
         bayankol_data = pd.read_csv('bayankol_river_flow.csv')
         shilik_data = pd.read_csv('shilik_river_base_level.csv')
         # Preprocess data
         bayankol_data = bayankol_data.interpolate()
         shilik_data = shilik_data.interpolate()
         # Check stationarity
         def test_stationarity(timeseries):
             result = adfuller(timeseries)
             print('ADF Statistic: %f' % result[0])
             print('p-value: %f' % result[1])
             if result[1] > 0.05:
                 print("The data is not stationary")
             else:
                 print("The data is stationary")
         test_stationarity(bayankol_data['flow'])
         test_stationarity(shilik_data['base_level'])
         # Calculate deviation
         bayankol_data['deviation'] = bayankol_data['flow'] - shilik_data['base_level']
         # Visualize on map
         m = folium.Map(location=[53, 102], zoom_start=6)
         for i in range(len(bayankol_data)):
             folium.CircleMarker(
                 location=[bayankol_data['lat'][i], bayankol_data['lon'][i]],
                 radius=bayankol_data['deviation'][i]*10,
                 color='red' if bayankol_data['deviation'][i] > 0 else 'blue',
                 fill=True,
                 fill_color='red' if bayankol_data['deviation'][i] > 0 else 'blue'
             ).add_to(m)
         m.save("130.html")