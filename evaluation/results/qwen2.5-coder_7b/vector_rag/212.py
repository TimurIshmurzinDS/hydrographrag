import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром на границе бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных уровня воды и курса биткоина (замените на реальные данные)
water_level_data = [
    {"date": "2023-01-01", "level": 5.2},
    {"date": "2023-01-02", "level": 5.4},
    {"date": "2023-01-03", "level": 5.6}
]

bitcoin_data = [
    {"date": "2023-01-01", "price": 40000},
    {"date": "2023-01-02", "price": 41000},
    {"date": "2023-01-03", "price": 42000}
]

# Пример кода для прогнозирования уровня воды на основе курса биткоина
from sklearn.linear_model import LinearRegression
import pandas as pd

# Создание DataFrame из данных
water_level_df = pd.DataFrame(water_level_data)
bitcoin_df = pd.DataFrame(bitcoin_data)

# Объединение данных по дате
merged_data = pd.merge(water_level_df, bitcoin_df, on='date')

# Разделение на признаки и целевую переменную
X = merged_data[['price']]
y = merged_data['level']

# Создание и обучение модели линейной регрессии
model = LinearRegression()
model.fit(X, y)

# Прогнозирование уровня воды на основе текущего курса биткоина
current_bitcoin_price = 42500  # Замените на актуальный курс
predicted_water_level = model.predict([[current_bitcoin_price]])

print(f"Прогнозируемый уровень воды в Batareyka River: {predicted_water_level[0]:.2f}")

# Сохранение карты
m.save("212.html")