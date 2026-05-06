import pandas as pd
import matplotlib.pyplot as plt
import folium

# Загрузить данные о уровне воды из CSV файлов
data_ili = pd.read_csv("ili_water_level.csv", index_col="date")
data_karatal = pd.read_csv("karatal_water_level.csv", index_col="date")

# Вычислить статистические показатели
mean_ili = data_ili["level"].mean()
std_ili = data_ili["level"].std()
cv_ili = std_ili / mean_ili * 100

mean_karatal = data_karatal["level"].mean()
std_karatal = data_karatal["level"].std()
cv_karatal = std_karatal / mean_karatal * 100

# Визуализация данных
plt.figure(figsize=(12,6))
plt.plot(data_ili.index, data_ili["level"], label="Ili")
plt.plot(data_karatal.index, data_karatal["level"], label="Karatal")
plt.xlabel("Дата")
plt.ylabel("Уровень воды (м)")
plt.title("Сравнение уровня воды в реках Или и Каратал")
plt.legend()

# Сохранить график
plt.savefig("water_levels.png")

# Создать карту с Folium
m = folium.Map(location=[43.25, 78.0], zoom_start=7)

folium.Marker([43.25, 78.0], popup="Река Или").add_to(m)
folium.Marker([42.9, 76.5], popup="Река Каратал").add_to(m)

# Сохранить карту
m.save("150.html")

print(f"Средний уровень воды в реке Или: {mean_ili:.2f} м")
print(f"Стандартное отклонение уровня воды в реке Или: {std_ili:.2f} м")
print(f"Коэффициент вариации уровня воды в реке Или: {cv_ili:.2f}%")

print(f"\nСредний уровень воды в реке Каратал: {mean_karatal:.2f} м")
print(f"Стандартное отклонение уровня воды в реке Каратал: {std_karatal:.2f} м")
print(f"Коэффициент вариации уровня воды в реке Каратал: {cv_karatal:.2f}%")