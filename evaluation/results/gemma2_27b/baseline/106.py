import pandas as pd
import folium

# Загрузка данных о уровнях воды из CSV файла
water_levels = pd.read_csv("water_levels.csv")

# Загрузка данных о потреблении воды для орошения
irrigation_needs = pd.read_csv("irrigation_needs.csv")

# Расчет доступного объема воды (упрощенная версия)
available_water = water_levels["level"] * 100 # Умножаем уровень на 100 для приблизительного расчета

# Сравнение с потребностью
if available_water >= irrigation_needs:
    print("Достаточно воды для орошения.")
else:
    print("Недостаточно воды для орошения.")

# Создание карты
m = folium.Map(location=[42.5, 76], zoom_start=8)

# Добавление данных о уровнях воды на карту
for index, row in water_levels.iterrows():
    folium.CircleMarker(location=[row["latitude"], row["longitude"]], radius=5, fill=True, color="green" if row["level"] >= 10 else "red").add_to(m)

# Сохранение карты
m.save("106.html")