python
         import pandas as pd
         from sklearn.linear_model import LinearRegression
         import folium
         # Load data
         koksu = pd.read_csv('koksu_river.csv')
         byzhy = pd.read_csv('byzhy_river.csv')
         # Preprocess data
         koksu['min_level'] = koksu['min_level'].fillna(koksu['min_level'].mean())
         byzhy['min_level'] = byzhy['min_level'].fillna(byzhy['min_level'].mean())
         # Model data
         X_koksu = koksu[['year']]
         y_koksu = koksu['min_level']
         model_koksu = LinearRegression().fit(X_koksu, y_koksu)
         X_byzhy = byzhy[['year']]
         y_byzhy = byzhy['min_level']
         model_byzhy = LinearRegression().fit(X_byzhy, y_byzhy)
         # Visualize data
         m = folium.Map(location=[55, 60], zoom_start=4)
         folium.PolyLine(locations=koksu[['lat', 'lon']].values, color='blue').add_to(m)
         folium.PolyLine(locations=byzhy[['lat', 'lon']].values, color='red').add_to(m)
         for i in range(len(koksu)):
             folium.CircleMarker(location=[koksu.iloc[i]['lat'], koksu.iloc[i]['lon']], radius=koksu.iloc[i]['min_level']/10, color='blue').add_to(m)
         for i in range(len(byzhy)):
             folium.CircleMarker(location=[byzhy.iloc[i]['lat'], byzhy.iloc[i]['lon']], radius=byzhy.iloc[i]['min_level']/10, color='red').add_to(m)
         m.save("208.html")