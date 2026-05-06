import pandas as pd
import matplotlib.pyplot as plt
import folium
import numpy as np

# 1. Подготовка данных
# Создаем синтетические данные для сезонного расхода воды (м3/с)
# Типичный цикл: рост весной (таяние снегов), спад осенью/зимой
months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 
          'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

# Данные для реки Или (крупная река, значительный сток)
ili_discharge = [150, 180, 400, 800, 1200, 1100, 900, 700, 500, 300, 200, 160]
# Данные для реки Шыжын (меньшая река, более резкие колебания)
shyzhyn_discharge = [20, 25, 60, 150, 250, 200, 120, 80, 50, 30, 25, 20]

df = pd.DataFrame({
    'Month': months,
    'Ili_River': ili_discharge,
    'Shyzhyn_River': shyzhyn_discharge
})

# 2. Сравнительный анализ (Расчеты)
avg_ili = df['Ili_River'].mean()
avg_shyzhyn = df['Shyzhyn_River'].mean()
max_ili = df['Ili_River'].max()
max_shyzhyn = df['Shyzhyn_River'].max()

print(f"Средний расход Или: {avg_ili:.2f} м3/с (Пик: {max_ili})")
print(f"Средний расход Шыжын: {avg_shyzhyn:.2f} м3/с (Пик: {max_shyzhyn})")

# 3. Визуализация временных рядов (Гидрограф)
plt.figure(figsize=(12, 6))
plt.plot(df['Month'], df['Ili_River'], marker='o', label='Ili River', color='blue', linewidth=2)
plt.plot(df['Month'], df['Shyzhyn_River'], marker='s', label='Shyzhyn River', color='green', linewidth=2)
plt.title('Сравнение сезонного расхода воды в реках Или и Шыжын', fontsize=14)
plt.xlabel('Месяц')
plt.ylabel('Расход воды (м3/с)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig("discharge_comparison.png")
plt.show()

# 4. Геопространственная визуализация
# Координаты (приблизительные для демонстрации)
locations = {
    "Ili River": [43.5, 79.5], 
    "Shyzhyn River": [43.2, 78.8]
}

# Создание карты
m = folium.Map(location=[43.3, 79.1], zoom_start=7, tiles='OpenStreetMap')

# Добавление маркеров с информацией
for river, coords in locations.items():
    # Определяем средний расход для конкретной реки
    avg_val = avg_ili if river == "Ili River" else avg_shyzhyn
    popup_text = f"<b>{river}</b><br>Средний расход: {avg_val:.2f} м3/с"
    
    folium.Marker(
        location=coords,
        popup=folium.Popup(popup_text, max_width=200),
        tooltip=river,
        icon=folium.Icon(color='blue' if river == "Ili River" else 'green', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("160.html")

print("Результаты сохранены: график 'discharge_comparison.png' и карта '160.html'")