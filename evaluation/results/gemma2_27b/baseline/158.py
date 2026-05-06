import pandas as pd
import matplotlib.pyplot as plt
import folium

# Загрузка данных о уровне воды из CSV файла
data = pd.read_csv("river_data.csv", index_col="Date")

# Определение опасного уровня для каждой реки
dangerous_level_Bayankol = 100 # Пример, заменить на реальное значение
dangerous_level_Sarykan = 80  # Пример, заменить на реальное значение

# Вычисление количества дней, когда уровень воды превышал опасный порог
dangerous_days_Bayankol = (data["Bayankol"] > dangerous_level_Bayankol).sum()
dangerous_days_Sarykan = (data["Sarykan"] > dangerous_level_Sarykan).sum()

# Вывод результатов
print(f"Количество дней, когда уровень воды в реке Bayankol превышал опасный порог: {dangerous_days_Bayankol}")
print(f"Количество дней, когда уровень воды в реке Sarykan превышал опасный порог: {dangerous_days_Sarykan}")

# Визуализация данных на карте

m = folium.Map(location=[45.0, 80.0], zoom_start=7)
folium.Marker(location=[45.2, 81.0], popup="Bayankol River").add_to(m)
folium.Marker(location=[44.8, 82.0], popup="Sarykan River").add_to(m)

# Сохранение карты в HTML файл
m.save("158.html")