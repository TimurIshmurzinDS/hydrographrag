python
         import pandas as pd
         from geopy.geocoders import Nominatim
         from sklearn.model_selection import train_test_split
         from sklearn.ensemble import RandomForestRegressor
         from sklearn.metrics import mean_squared_error
         import folium
         # Load data
         sensor_data = pd.read_csv('sensor_data.csv')
         ethereum_prices = pd.read_csv('ethereum_prices.csv')
         # Preprocess data
         sensor_data = sensor_data.dropna()
         ethereum_prices = ethereum_prices.dropna()
         # Geocode sensor locations
         geolocator = Nominatim(user_agent="ethereum_price_prediction")
         def get_coordinates(location):
             loc = geolocator.geocode(location)
             return (loc.latitude, loc.longitude)
         sensor_data[['lat', 'lon']] = sensor_data['location'].apply(get_coordinates).apply(pd.Series)
         # Create spatial features
         def calculate_distance(row):
             return ((row['lat'] - city_center_lat)**2 + (row['lon'] - city_center_lon)**2)**0.5
         sensor_data['distance_to_city_center'] = sensor_data.apply(calculate_distance, axis=1)
         # Merge data
         merged_data = pd.merge(sensor_data, ethereum_prices, on='date')
         # Split data into training and testing sets
         X = merged_data[['reading', 'distance_to_city_center']]
         y = merged_data['price']
         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
         # Train model
         model = RandomForestRegressor()
         model.fit(X_train, y_train)
         # Evaluate model
         predictions = model.predict(X_test)
         mse = mean_squared_error(y_test, predictions)
         print('Mean Squared Error:', mse)
         # Visualize results on map
         m = folium.Map(location=[city_center_lat, city_center_lon], zoom_start=12)
         for i in range(len(X_test)):
             folium.CircleMarker([X_test.iloc[i]['lat'], X_test.iloc[i]['lon']], radius=5, color='red', fill=True, fill_color='red', popup=f'Predicted Price: {predictions[i]}').add_to(m)
         m.save("213.html")