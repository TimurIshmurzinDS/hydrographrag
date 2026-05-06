python
        import pandas as pd
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LinearRegression
        import folium

        # Load data
        bayankol_data = pd.read_csv('bayankol_river_data.csv')
        sarykan_data = pd.read_csv('sarykan_river_data.csv')

        # Preprocess data
        def preprocess(data):
            data['month'] = pd.to_datetime(data['date']).dt.month
            return data[['water_level', 'flow', 'month']]

        bayankol_data = preprocess(bayankol_data)
        sarykan_data = preprocess(sarykan_data)

        # Train model
        def train_model(data):
            X = data[['water_level', 'month']]
            y = data['flow']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
            model = LinearRegression()
            model.fit(X_train, y_train)
            return model

        bayankol_model = train_model(bayankol_data)
        sarykan_model = train_model(sarykan_data)

        # Predict flood risks
        def predict_flood_risk(data, model):
            data['predicted_flow'] = model.predict(data[['water_level', 'month']])
            data['flood_risk'] = data['predicted_flow'].apply(lambda x: 'high' if x > data['flow'].mean() + 2*data['flow'].std() else 'low')
            return data

        bayankol_data = predict_flood_risk(bayankol_data, bayankol_model)
        sarykan_data = predict_flood_risk(sarykan_data, sarykan_model)

        # Visualize results on map
        m = folium.Map(location=[55, 90], zoom_start=4)

        for i, row in bayankol_data[bayankol_data['flood_risk'] == 'high'].iterrows():
            folium.CircleMarker(location=[row['lat'], row['lon']], radius=10, color='red').add_to(m)

        for i, row in sarykan_data[sarykan_data['flood_risk'] == 'high'].iterrows():
            folium.CircleMarker(location=[row['lat'], row['lon']], radius=10, color='red').add_to(m)

        m.save("158.html")