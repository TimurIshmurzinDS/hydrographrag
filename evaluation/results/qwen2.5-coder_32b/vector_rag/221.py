import geopandas as gpd
import folium
from shapely import wkt
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Dos River
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о уровне воды (замените это на реальные данные)
data = {
    'Date_water_level_Value': pd.date_range(start='1/1/2020', periods=365),
    'Water_level_Valuecm': [100 + 10 * i % 365 for i in range(365)]
}

# Преобразование данных в DataFrame
df = pd.DataFrame(data)
df.set_index('Date_water_level_Value', inplace=True)

# Построение модели ARIMA
model = ARIMA(df['Water_level_Valuecm'], order=(5,1,0))
model_fit = model.fit()

# Прогнозирование уровня воды на 30 дней вперед
forecast = model_fit.forecast(steps=30)
forecast_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=30)

# Визуализация результатов
plt.figure(figsize=(12,6))
plt.plot(df.index, df['Water_level_Valuecm'], label='Исторические данные')
plt.plot(forecast_dates, forecast, label='Прогноз', color='red')
plt.title('Прогноз уровня воды в реке Dos River')
plt.xlabel('Дата')
plt.ylabel('Уровень воды (см)')
plt.legend()
plt.show()

# Сохранение карты
m.save("221.html")