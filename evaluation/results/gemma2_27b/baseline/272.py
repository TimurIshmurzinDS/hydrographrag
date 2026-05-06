import pandas as pd
import folium

# Загрузить данные из CSV файла
data = pd.read_csv("inflation_data.csv")

# Рассчитать темпы инфляции
data["inflation_rate"] = (data["current_year_inflation"] - data["previous_year_inflation"]) / data["previous_year_inflation"] * 100

# Создать карту Folium
m = folium.Map(location=[42.5, 76], zoom_start=8)

# Добавить точки на карту с цветом в зависимости от темпа инфляции
for index, row in data.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=5,
        color="green" if row["inflation_rate"] < 5 else "yellow" if 5 <= row["inflation_rate"] < 10 else "red",
        fill=True,
    ).add_to(m)

# Сохранить карту
m.save("272.html")