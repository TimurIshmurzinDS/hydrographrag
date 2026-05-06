python
        import pandas as pd
        from statsmodels.tsa.seasonal import seasonal_decompose
        import matplotlib.pyplot as plt
        import folium

        # Load data
        shilik_data = pd.read_csv('shilik_river_flow.csv', index_col='Date', parse_dates=True)
        shyzhyn_data = pd.read_csv('shyzhyn_river_flow.csv', index_col='Date', parse_dates=True)

        # Data cleaning (handle missing values and outliers here)

        # Seasonal decomposition for Shilik River
        shilik_decomposition = seasonal_decompose(shilik_data['Flow'], model='additive')
        shilik_seasonal = shilik_decomposition.seasonal
        shilik_amplitude = shilik_seasonal.max() - shilik_seasonal.min()

        # Seasonal decomposition for Shyzhyn River
        shyzhyn_decomposition = seasonal_decompose(shyzhyn_data['Flow'], model='additive')
        shyzhyn_seasonal = shyzhyn_decomposition.seasonal
        shyzhyn_amplitude = shyzhyn_seasonal.max() - shyzhyn_seasonal.min()

        print(f"Shilik River predicted seasonal flow amplitude: {shilik_amplitude}")
        print(f"Shyzhyn River predicted seasonal flow amplitude: {shyzhyn_amplitude}")

        # Visualization on map using folium (assuming rivers' coordinates are available)
        m = folium.Map(location=[55, 37], zoom_start=6)
        folium.Marker([55.1287, 61.4025], popup=f"Shilik River Amplitude: {shilik_amplitude}").add_to(m)
        folium.Marker([53.9022, 37.5022], popup=f"Shyzhyn River Amplitude: {shyzhyn_amplitude}").add_to(m)
        m.save("157.html")