import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузка данных о расходе воды
df = pd.read_csv("river_discharge_data.csv")

# Преобразование данных в GeoDataFrame
geometry = [Point(x, y) for x, y in zip(df["longitude"], df["latitude"])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

# Выбор модели (например, линейная регрессия)
from sklearn.linear_model import LinearRegression

# Обучение модели на исторических данных
X = df[["month", "previous_year_discharge"]]
y = df["discharge"]
model = LinearRegression()
model.fit(X, y)

# Прогнозирование риска затопления
future_data = pd.DataFrame({"month": [6], "previous_year_discharge": [100]})
predicted_discharge = model.predict(future_data)

# Визуализация результатов на карте
m = folium.Map(location=[df["latitude"].mean(), df["longitude"].mean()], zoom_start=8)

# Добавление точек с риском затопления
for index, row in gdf.iterrows():
    folium.Marker(location=(row["geometry"][1], row["geometry"][0]), popup=f"Predicted Discharge: {predicted_discharge[0]}").add_to(m)

# Сохранение карты
m.save("85.html")