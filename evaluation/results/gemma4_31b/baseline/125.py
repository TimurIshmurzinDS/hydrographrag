import pandas as pd
import folium
import numpy as np

# 1. Подготовка данных (Симуляция гидрологических данных за 5 лет)
data = {
    'Year': [2019, 2020, 2021, 2022, 2023] * 2,
    'River': ['Tekes River'] * 5 + ['Bayankol River'] * 5,
    'Discharge': [
        # Tekes River: умеренный рост
        12.5, 13.1, 12.8, 14.2, 15.5, 
        # Bayankol River: значительный скачок в последний год
        8.2, 8.5, 7.9, 8.1, 12.4 
    ]
}

df = pd.DataFrame(data)

# 2. Расчет среднего и текущего увеличения
results = {}
rivers = df['River'].unique()

for river in rivers:
    river_data = df[df['River'] == river]
    avg_discharge = river_data['Discharge'].mean()
    current_discharge = river_data.iloc[-1]['Discharge']
    increase = current_discharge - avg_discharge
    results[river] = {
        'avg': avg_discharge,
        'current': current_discharge,
        'increase': increase
    }

# Определение реки с наибольшим увеличением
winner = max(results, key=lambda x: results[x]['increase'])
print(f"Наибольшее увеличение расхода воды показала река: {winner}")
print(f"Прирост относительно среднего: {results[winner]['increase']:.2f} m3/s")

# 3. Геопространственная визуализация
# Приблизительные координаты для визуализации (Центральная Азия)
coords = {
    'Tekes River': [44.5, 78.0],
    'Bayankol River': [44.0, 65.0]
}

# Создание карты
m = folium.Map(location=[44.2, 71.5], zoom_start=5, tiles='CartoDB positron')

for river, info in results.items():
    color = 'green' if river == winner else 'blue'
    icon_color = 'orange' if river == winner else 'blue'
    
    # Создание всплывающего окна с данными
    popup_text = (
        f"<b>{river}</b><br>"
        f"Средний расход: {info['avg']:.2f} m3/s<br>"
        f"Текущий расход: {info['current']:.2f} m3/s<br>"
        f"Увеличение: {info['increase']:.2f} m3/s"
    )
    
    folium.Marker(
        location=coords[river],
        popup=popup_text,
        tooltip=f"{river} (Increase: {info['increase']:.2f})",
        icon=folium.Icon(color=icon_color, icon='info-sign')
    ).add_to(m)

# Добавление текстового пояснения на карту
folium.Marker(
    location=[44.2, 71.5],
    icon=folium.DivIcon(html=f"""<div style="font-family: Arial; color: black; font-weight: bold; 
                                background: white; padding: 10px; border: 2px solid black;">
                                Результат: {winner} показала наибольший рост</div>""")
).add_to(m)

# Сохранение карты
m.save("125.html")