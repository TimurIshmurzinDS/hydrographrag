import geopandas as gpd
import folium
from shapely import wkt
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с использованием центроида shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных (замените на реальные данные)
data = {
    'Date_water_level_Value': pd.date_range(start='1/1/2020', periods=100, freq='D'),
    'Water_level_Valuecm': [50 + 10 * i for i in range(100)]
}

# Преобразование данных в DataFrame
df = pd.DataFrame(data)
df.set_index('Date_water_level_Value', inplace=True)

# Визуализация временного ряда
plt.figure(figsize=(12, 6))
plt.plot(df['Water_level_Valuecm'], label='Уровень воды (см)')
plt.title('Исторический уровень воды в реке Kurty River')
plt.xlabel('Дата')
plt.ylabel('Уровень воды (см)')
plt.legend()
plt.show()

# Обучение модели ARIMA
model = ARIMA(df['Water_level_Valuecm'], order=(5,1,0))
model_fit = model.fit()

# Прогнозирование на следующие 7 дней
forecast = model_fit.forecast(steps=7)

# Визуализация прогноза
plt.figure(figsize=(12, 6))
plt.plot(df['Water_level_Valuecm'], label='Исторический уровень воды (см)')
plt.plot(forecast, label='Прогнозируемый уровень воды (см)', color='red')
plt.title('Прогноз уровня воды в реке Kurty River на следующие 7 дней')
plt.xlabel('Дата')
plt.ylabel('Уровень воды (см)')
plt.legend()
plt.show()

# Сохранение карты
m.save("57.html")