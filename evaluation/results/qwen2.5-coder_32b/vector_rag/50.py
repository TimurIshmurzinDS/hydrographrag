import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и преобразование CRS
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с использованием центроида бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о уровне воды (замените на реальные данные)
water_level_data = [
    {"Date_water_level_Value": "2018-01-01", "Water_level_Valuecm": 150},
    {"Date_water_level_Value": "2018-02-01", "Water_level_Valuecm": 160},
    # Добавьте остальные данные за последние 5 лет
]

# Преобразование данных в DataFrame для анализа
import pandas as pd
from datetime import datetime

df = pd.DataFrame(water_level_data)
df['Date_water_level_Value'] = pd.to_datetime(df['Date_water_level_Value'])
df.set_index('Date_water_level_Value', inplace=True)

# Построение модели ARIMA
from statsmodels.tsa.arima.model import ARIMA

model = ARIMA(df['Water_level_Valuecm'], order=(5,1,0))
model_fit = model.fit()

# Прогнозирование уровня воды на 6 месяцев вперед
forecast = model_fit.forecast(steps=6)
print(forecast)

# Сохранение карты
m.save("50.html")