python
import pandas as pd
import matplotlib.pyplot as plt
import folium

# Загрузить данные о уровнях рек из CSV файлов
emel_data = pd.read_csv("emel_levels.csv", index_col="date")
turgen_data = pd.read_csv("turgen_levels.csv", index_col="date")

# Определить порог экстремального понижения (например, 2 стандартных отклонения ниже среднего)
emel_mean = emel_data["level"].mean()
emel_std = emel_data["level"].std()
threshold = emel_mean - 2 * emel_std

# Расчитать количество экстремальных межени в Emel
emel_extreme_count = len(emel_data[emel_data["level"] < threshold])

# Повторить для Turgen
turgen_mean = turgen_data["level"].mean()
turgen_std = turgen_data["level"].std()
turgen_threshold = turgen_mean - 2 * turgen_std
turgen_extreme_count = len(turgen_data[turgen_data["level"] < turgen_threshold])

# Вывести результат
print("Частота экстремальных межени в Emel:", emel_extreme_count)
print("Частота экстремальных межени в Turgen:", turgen_extreme_count)

# Визуализация (необязательно)
plt.plot(emel_data["level"], label="Emel")
plt.plot(turgen_data["level"], label="Turgen")
plt.axhline(y=threshold, color="red", linestyle="--", label="Threshold")
plt.legend()
plt.show()

# Карта (необязательно)
m = folium.Map(location=[50, 60], zoom_start=8)
folium.Marker(location=[51.2, 61.4], popup="Emel").add_to(m)
folium.Marker(location=[52.3, 62.7], popup="Turgen").add_to(m)

m.save("207.html")