python
         import pandas as pd
         import folium
         from folium.plugins import MarkerCluster

         # Загрузка данных
         emel_data = pd.read_csv('emel_river_flow.csv')
         turgen_data = pd.read_csv('turgen_river_flow.csv')

         # Рассчет среднего и стандартного отклонения для Emel River
         emel_mean = emel_data['flow'].mean()
         emel_std = emel_data['flow'].std()

         # Рассчет среднего и стандартного отклонения для Turgen River
         turgen_mean = turgen_data['flow'].mean()
         turgen_std = turgen_data['flow'].std()

         # Сравнение изменчивости стока
         if emel_std > turgen_std:
             print("Emel River демонстрирует более значительную межгодовую изменчивость стока.")
         else:
             print("Turgen River демонстрирует более значительную межгодовую изменчивость стока.")

         # Создание карты с помощью folium (предполагается, что в данных есть координаты)
         m = folium.Map(location=[emel_data['lat'].mean(), emel_data['lon'].mean()], zoom_start=10)
         marker_cluster = MarkerCluster().add_to(m)
         for i, row in emel_data.iterrows():
             folium.Marker([row['lat'], row['lon']]).add_to(marker_cluster)
         m.save("202.html")