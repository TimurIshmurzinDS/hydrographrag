import geopandas as gpd
import pandas as pd
from sklearn.linear_model import LinearRegression
import folium

# Загрузка данных
delta = gpd.read_file("delta_boundary.shp")
biodiversity = pd.read_csv("biodiversity_data.csv")
water_extraction = pd.read_csv("water_extraction_data.csv")

# Создание модели
model = LinearRegression()
X = water_extraction["volume"].values.reshape(-1, 1)
y = biodiversity["biodiversity_index"]
model.fit(X, y)

# Прогнозирование изменения биоразнообразия
future_water_extraction = pd.DataFrame({"volume": [5000, 10000]})  
predicted_biodiversity = model.predict(future_water_extraction["volume"].values.reshape(-1, 1))

# Визуализация
m = folium.Map(location=[delta.geometry.y.mean(), delta.geometry.x.mean()], zoom_start=12)

folium.GeoJson(delta).add_to(m)

for index, row in biodiversity.iterrows():
    folium.CircleMarker(location=[row["latitude"], row["longitude"]], radius=5, color="green" if row["biodiversity_index"] > 3 else "red").add_to(m)

for index, row in water_extraction.iterrows():
    folium.Marker(location=[row["latitude"], row["longitude"]], popup=f"Volume: {row['volume']}").add_to(m)

m.save("191.html")