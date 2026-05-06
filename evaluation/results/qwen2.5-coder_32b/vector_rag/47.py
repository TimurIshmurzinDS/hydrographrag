import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна и преобразование CRS
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты folium с центром в центроиде бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть исторические данные о расходе воды в реке Шилик
# В реальном сценарии эти данные должны быть загружены из соответствующего источника
historical_data = {
    'date': pd.date_range(start='2023-01-01', periods=12, freq='M'),
    'discharge': [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160]
}

# Преобразование данных в DataFrame
import pandas as pd
df = pd.DataFrame(historical_data)
df.set_index('date', inplace=True)

# Построение модели SARIMA для предсказания расхода воды
from statsmodels.tsa.statespace.sarimax import SARIMAX

model = SARIMAX(df['discharge'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
model_fit = model.fit(disp=False)

# Предсказание расхода воды на следующий месяц
forecast = model_fit.forecast(steps=1)
print(f"Предсказанный расход воды в реке Шилик на следующий месяц: {forecast[0]:.2f} м³/с")

# Сохранение карты
m.save("47.html")