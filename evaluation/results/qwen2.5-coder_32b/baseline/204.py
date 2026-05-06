import pandas as pd
import matplotlib.pyplot as plt
import folium

# Предполагается, что у нас есть CSV файлы с историческими данными о дисcharges для обоих речных систем.
# Формат данных: Дата (YYYY-MM-DD), Discharge (куб. м/с)

# Шаг 1: Сбор и загрузка данных
byzhy_data = pd.read_csv('byzhy_discharge.csv', parse_dates=['Date'])
urzhar_data = pd.read_csv('urzhar_discharge.csv', parse_dates=['Date'])

# Шаг 2: Предварительная обработка данных
byzhy_data.set_index('Date', inplace=True)
urzhar_data.set_index('Date', inplace=True)

# Проверка на пропущенные значения и удаление их, если есть
byzhy_data.dropna(inplace=True)
urzhar_data.dropna(inplace=True)

# Шаг 3: Анализ временных рядов
# Вычисление среднего стока для каждого месяца
byzhy_monthly_avg = byzhy_data.resample('M').mean()
urzhar_monthly_avg = urzhar_data.resample('M').mean()

# Шаг 4: Визуализация данных
plt.figure(figsize=(12, 6))
plt.plot(byzhy_monthly_avg.index, byzhy_monthly_avg['Discharge'], label='Byzhy River', color='blue')
plt.plot(urzhar_monthly_avg.index, urzhar_monthly_avg['Discharge'], label='Urzhar River', color='green')
plt.title('Сравнение гидрологических режимов рек Byzhy и Urzhar')
plt.xlabel('Дата')
plt.ylabel('Сток (куб. м/с)')
plt.legend()
plt.grid(True)
plt.show()

# Шаг 5: Географическая визуализация
# Координаты рек (примерные значения, нужно заменить на точные)
byzhy_coords = [48.2319, 67.0819]  # примерные координаты Byzhy River
urzhar_coords = [50.0500, 73.3667]  # примерные координаты Urzhar River

# Создание карты с использованием folium
m = folium.Map(location=[49.18, 70.2], zoom_start=5)

# Добавление маркеров для рек
folium.Marker(byzhy_coords, popup='Byzhy River', tooltip='Средний сток: {:.2f} куб. м/с'.format(byzhy_monthly_avg['Discharge'].mean())).add_to(m)
folium.Marker(urzhar_coords, popup='Urzhar River', tooltip='Средний сток: {:.2f} куб. м/с'.format(urzhar_monthly_avg['Discharge'].mean())).add_to(m)

# Сохранение карты в HTML файл
m.save("204.html")