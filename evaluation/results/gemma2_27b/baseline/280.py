import pandas as pd
from geopy.geocoders import Nominatim
import folium

# 1. Загрузка данных
data = pd.read_csv("housing_costs.csv")

# 2. Предобработка данных (проверка на пропуски, формат времени)
# ...

# 3. Геокодирование
geolocator = Nominatim(timeout=10)
data["coordinates"] = data["city"].apply(lambda x: geolocator.geocode(x).address)
data[["latitude", "longitude"]] = data["coordinates"].str.extract(r"\((.*)\)", expand=True).astype(float)

# 4. Создание модели (например, линейная регрессия)
from sklearn.linear_model import LinearRegression
X = data["year"].values.reshape(-1, 1)
y = data["cost"].values
model = LinearRegression()
model.fit(X, y)

# 5. Визуализация на карте Folium
m = folium.Map(location=[40, 30], zoom_start=5)
for index, row in data.iterrows():
    folium.Circle(
        location=[row["latitude"], row["longitude"]],
        radius=10000 * (row["cost"] / 1000),
        color="green" if row["cost"] < 500 else "red",
        fill=True,
    ).add_to(m)

# Сохранение карты
m.save("280.html")