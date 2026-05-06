import geopandas as gpd
import folium
from shapely import wkt
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Загрузка и преобразование данных
data = pd.read_csv('path_to_your_data.csv')  # Замените на путь к вашему CSV файлу с данными уровня воды
data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)

# Проверка пропущенных значений
print("Пропущенные значения:", data.isnull().sum())

# Удаление пропущенных значений
data.dropna(inplace=True)

# Визуализация временного ряда
plt.figure(figsize=(10, 5))
plt.plot(data['water_level_value'], label='Уровень воды')
plt.title('Временной ряд уровня воды в Dos River')
plt.xlabel('Дата')
plt.ylabel('Уровень воды')
plt.legend()
plt.show()

# Обучение модели ARIMA
model = ARIMA(data['water_level_value'], order=(5,1,0))  # Выберите оптимальные параметры (p,d,q)
model_fit = model.fit()

# Прогнозирование будущих значений
forecast_steps = 30  # Количество шагов прогнозирования
forecast = model_fit.forecast(steps=forecast_steps)

# Визуализация прогноза
plt.figure(figsize=(10, 5))
plt.plot(data['water_level_value'], label='Исторические данные')
plt.plot(forecast.index, forecast, label='Прогноз', color='red')
plt.title('Прогноз уровня воды в Dos River')
plt.xlabel('Дата')
plt.ylabel('Уровень воды')
plt.legend()
plt.show()

# Создание карты
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10, tiles='CartoDB positron')

# Добавление базина
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.to_crs(epsg=4326, inplace=True)
folium.GeoJson(basin_data.geometry, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Сохранение карты
m.save("221.html")