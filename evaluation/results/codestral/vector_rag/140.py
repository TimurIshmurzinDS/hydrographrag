python
       import geopandas as gpd
       import folium
       from shapely import wkt
       import pandas as pd
       import matplotlib.pyplot as plt

       # Создаем датафрейм с данными о наблюдениях
       data = {
           'Observation': ['Observation_1', 'Observation_2200'],
           'Date': ['Date_water_level_Value_1', 'Date_water_level_Value_2200'],
           'Water_Level': ['Water_level_Value_1', 'Water_level_Value_2200']
       }
       df = pd.DataFrame(data)

       # Анализируем стабильность связи датчиков
       plt.figure(figsize=(10, 6))
       plt.plot(df['Date'], df['Water_Level'], marker='o')
       plt.title('Стабильность связи датчиков на реке Токыраун')
       plt.xlabel('Дата')
       plt.ylabel('Уровень воды')
       plt.xticks(rotation=45)
       plt.grid(True)
       plt.show()