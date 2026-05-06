python
         import pandas as pd
         import numpy as np
         from sklearn.model_selection import train_test_split
         from sklearn.linear_model import LinearRegression
         import folium
         # Load data
         data = pd.read_csv('batareyka_river_data.csv')
         # Preprocess data
         data = data.dropna()
         data['rainfall'] = np.log(data['rainfall'])
         data['water_level'] = (data['water_level'] - data['water_level'].mean()) / data['water_level'].std()
         # Split data into training and testing sets
         X = data[['rainfall', 'water_level']]
         y = data['discharge']
         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
         # Train model
         model = LinearRegression()
         model.fit(X_train, y_train)
         # Predict discharge during flood period
         flood_data = data[data['flood'] == 1]
         X_flood = flood_data[['rainfall', 'water_level']]
         y_pred = model.predict(X_flood)
         # Visualize results on map
         m = folium.Map(location=[55.75, 37.62], zoom_start=10)
         for i in range(len(y_pred)):
             folium.CircleMarker(location=[flood_data.iloc[i]['lat'], flood_data.iloc[i]['lon']],
                                 radius=y_pred[i]*5,
                                 color='red',
                                 fill=True,
                                 fill_color='red').add_to(m)
         m.save("20.html")