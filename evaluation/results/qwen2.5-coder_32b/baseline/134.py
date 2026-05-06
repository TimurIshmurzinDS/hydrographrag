import pandas as pd
import numpy as np
import folium

# Предполагается, что у нас есть CSV файлы с данными о дисcharges для каждой реки.
# Формат данных: Дата (YYYY-MM-DD), Discharge (куб. м/с)

# Загрузка данных
bayankol_data = pd.read_csv('bayankol_discharge.csv', parse_dates=['Date'])
kishi_almaty_data = pd.read_csv('kishi_almaty_discharge.csv', parse_dates=['Date'])

# Предварительная обработка данных (проверка на пропуски и аномалии)
bayankol_data.dropna(inplace=True)
kishi_almaty_data.dropna(inplace=True)

# Вычисление волатильности (стандартное отклонение) для временных рядов дисcharges
bayankol_volatility = bayankol_data['Discharge'].std()
kishi_almaty_volatility = kishi_almaty_data['Discharge'].std()

print(f"Волатильность стока воды в реке Bayankol River: {bayankol_volatility}")
print(f"Волатильность стока воды в реке Kishi Almaty River: {kishi_almaty_volatility}")

# Сравнение результатов
if bayankol_volatility > kishi_almaty_volatility:
    print("Волатильность стока воды в реке Bayankol River выше, чем в реке Kishi Almaty River.")
else:
    print("Волатильность стока воды в реке Kishi Almaty River не ниже, чем в реке Bayankol River.")

# Визуализация данных на карте
m = folium.Map(location=[45.0, 78.0], zoom_start=6)  # Координаты примерные

# Добавление маркеров для местоположения рек
folium.Marker(
    location=[43.2194, 77.1855],  # Примерные координаты Bayankol River
    popup=f"Bayankol River\nВолатильность: {bayankol_volatility:.2f}",
    icon=folium.Icon(color='blue')
).add_to(m)

folium.Marker(
    location=[43.1958, 76.9061],  # Примерные координаты Kishi Almaty River
    popup=f"Kishi Almaty River\nВолатильность: {kishi_almaty_volatility:.2f}",
    icon=folium.Icon(color='red')
).add_to(m)

# Сохранение карты в HTML файл
m.save("134.html")