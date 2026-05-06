python
         import pandas as pd
         import geopandas as gpd
         from scipy import stats
         import folium

         # Загрузка данных
         water_levels = pd.read_csv('water_levels.csv')
         ecosystems = gpd.read_file('ecosystems.shp')

         # Анализ связи между уровнем воды и состоянием экосистем
         correlation = water_levels['level'].corr(ecosystems['health_index'])

         # Оценка биоразнообразия в каждой экосистеме (предполагается наличие соответствующего индекса)
         ecosystems['diversity_score'] = calculate_diversity(ecosystems)  # Заменить на фактический метод оценки биоразнообразия

         # Визуализация результатов на карте
         m = folium.Map(location=[ecosystems['geometry'].centroid.y.mean(), ecosystems['geometry'].centroid.x.mean()], zoom_start=10)

         for idx, row in ecosystems.iterrows():
             folium.CircleMarker(
                 location=[row['geometry'].centroid.y, row['geometry'].centroid.x],
                 radius=row['diversity_score']*5,  # Масштабирование для лучшей визуализации
                 color='blue',
                 fill=True,
                 fill_color='blue'
             ).add_to(m)

         m.save("181.html")