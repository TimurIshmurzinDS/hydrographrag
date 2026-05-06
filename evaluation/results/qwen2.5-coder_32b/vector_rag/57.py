import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна и преобразование в CRS EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs(epsg=4326)

# Инициализация карты folium с центром в центроиде бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о уровне воды в реке Kurty River (для демонстрации)
water_level_data = [
    {"Date_water_level_Value": "2023-01-01", "Water_level_Valuecm": 150},
    {"Date_water_level_Value": "2023-01-02", "Water_level_Valuecm": 152},
    {"Date_water_level_Value": "2023-01-03", "Water_level_Valuecm": 155},
    {"Date_water_level_Value": "2023-01-04", "Water_level_Valuecm": 160},
    {"Date_water_level_Value": "2023-01-05", "Water_level_Valuecm": 165},
    # Добавьте больше данных для более точного прогнозирования
]

# Преобразование данных в формат pandas DataFrame
import pandas as pd
df = pd.DataFrame(water_level_data)
df['Date_water_level_Value'] = pd.to_datetime(df['Date_water_level_Value'])
df.set_index('Date_water_level_Value', inplace=True)

# Построение модели ARIMA для прогнозирования уровня воды
from statsmodels.tsa.arima.model import ARIMA

model = ARIMA(df['Water_level_Valuecm'], order=(5,1,0))
model_fit = model.fit()

# Прогнозирование уровня воды на 7 дней вперед
forecast = model_fit.forecast(steps=7)
print("Прогноз уровня воды на следующие 7 дней:")
print(forecast)

# Сохранение карты
m.save("57.html")