import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о уровне воды (заменить на реальные данные)
water_level_data = [
    {"Date_water_level_Value": "2023-01-01", "Water_level_Valuecm": 150},
    {"Date_water_level_Value": "2023-01-02", "Water_level_Valuecm": 152},
    {"Date_water_level_Value": "2023-01-03", "Water_level_Valuecm": 148},
    # Добавьте больше данных по мере необходимости
]

# Пример простой модели предсказания уровня воды (линейная регрессия)
import pandas as pd
from sklearn.linear_model import LinearRegression

# Преобразование данных в DataFrame
df = pd.DataFrame(water_level_data)
df['Date_water_level_Value'] = pd.to_datetime(df['Date_water_level_Value'])
df['Day_of_year'] = df['Date_water_level_Value'].dt.dayofyear

# Обучение модели
X = df[['Day_of_year']]
y = df['Water_level_Valuecm']
model = LinearRegression().fit(X, y)

# Пример предсказания уровня воды на следующий день
next_day = pd.DataFrame({'Day_of_year': [df['Day_of_year'].max() + 1]})
predicted_water_level = model.predict(next_day)[0]

# Вывод предсказанного значения уровня воды
print(f"Предсказанный уровень воды на следующий день: {predicted_water_level} см")

# Сохранение карты
m.save("236.html")