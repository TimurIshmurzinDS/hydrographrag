import geopandas as gpd
import folium
from shapely import wkt

# Загрузка географических данных о бассейне реки Dos River
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с использованием центроида бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание искусственных данных о уровнях воды (пример)
import pandas as pd
import numpy as np

np.random.seed(42)
dates = pd.date_range(start='1/1/2023', periods=365, freq='D')
water_levels_cm = 100 + 10 * np.sin(np.linspace(0, 2 * np.pi, len(dates))) + 5 * np.random.randn(len(dates))
eth_prices = 1000 + 50 * np.cos(np.linspace(0, 4 * np.pi, len(dates))) + 10 * np.random.randn(len(dates))

data = pd.DataFrame({
    'Date': dates,
    'Water_level_Valuecm': water_levels_cm,
    'Ethereum_Price': eth_prices
})

# Простая модель линейной регрессии для прогнозирования цен на Ethereum
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

X = data[['Water_level_Valuecm']]
y = data['Ethereum_Price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)

# Прогнозирование цен на основе тестовых данных
data['Predicted_Ethereum_Price'] = model.predict(X)

# Визуализация результатов на карте (пример: добавление маркеров с уровнями воды и прогнозируемыми ценами)
for _, row in data.iterrows():
    folium.Marker(
        location=[centroid.y, centroid.x],
        popup=f"Date: {row['Date']}, Water Level: {row['Water_level_Valuecm']} cm, Predicted Price: ${row['Predicted_Ethereum_Price']:.2f}",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты
m.save("213.html")