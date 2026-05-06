import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from datetime import datetime, timedelta

# 1. Симуляция гидрологических данных (так как реальные данные закрыты)
# Создаем временной ряд с марта по июнь
dates = pd.date_range(start="2023-03-01", end="2023-06-30")
n_days = len(dates)

def generate_flood_curve(peak_day, peak_value, noise_level=2):
    """Генерирует кривую половодья на основе нормального распределения"""
    x = np.arange(n_days)
    # Создаем колоколообразную кривую (Гауссиана) для имитации половодья
    curve = peak_value * np.exp(-((x - peak_day)**2) / (2 * 15**2))
    noise = np.random.normal(0, noise_level, n_days)
    return np.maximum(5, curve + noise) # Базовый расход не менее 5 м3/с

# Параметры для рек: Баянколь (более плавный), Лепсы (более резкий/горный характер)
bayankol_q = generate_flood_curve(peak_day=60, peak_value=45) # Пик в мае
lepsy_q = generate_flood_curve(peak_day=45, peak_value=80)    # Пик в апреле

df = pd.DataFrame({
    'Date': dates,
    'Bayankol_Q': bayankol_q,
    'Lepsy_Q': lepsy_q
})

# 2. Анализ динамики
def analyze_river(name, data):
    peak_val = data.max()
    peak_date = dates[data.argmax()]
    avg_val = data.mean()
    return {
        'River': name,
        'Peak_Discharge': round(peak_val, 2),
        'Peak_Date': peak_date.strftime('%Y-%m-%d'),
        'Average_Discharge': round(avg_val, 2)
    }

analysis_bayankol = analyze_river("Bayankol", df['Bayankol_Q'])
analysis_lepsy = analyze_river("Lepsy", df['Lepsy_Q'])

print("--- Анализ динамики половодья ---")
print(f"Река Баянколь: Пик {analysis_bayankol['Peak_Discharge']} м3/с от {analysis_bayankol['Peak_Date']}")
print(f"Река Лепсы: Пик {analysis_lepsy['Peak_Discharge']} м3/с от {analysis_lepsy['Peak_Date']}")

# 3. Визуализация гидрографов
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Bayankol_Q'], label='Bayankol River', color='blue', linewidth=2)
plt.plot(df['Date'], df['Lepsy_Q'], label='Lepsy River', color='green', linewidth=2)
plt.title('Динамика весеннего половодья (Расход воды Q)')
plt.xlabel('Дата')
plt.ylabel('Расход воды (м3/с)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig("flood_dynamics.png")
plt.close()

# 4. Геопространственная визуализация (Folium)
# Координаты (приблизительные для региона Жетысу, Казахстан)
coords = {
    'Bayankol': [44.5, 79.2],
    'Lepsy': [44.2, 78.5]
}

# Создание карты
m = folium.Map(location=[44.3, 78.8], zoom_start=8, tiles='OpenStreetMap')

# Добавление маркеров с результатами анализа
for river, pos in coords.items():
    res = analysis_bayankol if river == 'Bayankol' else analysis_lepsy
    popup_text = f"<b>Река {river}</b><br>Пик: {res['Peak_Discharge']} м3/с<br>Дата: {res['Peak_Date']}"
    
    folium.Marker(
        location=pos,
        popup=popup_text,
        tooltip=f"Пост мониторинга {river}",
        icon=folium.Icon(color='blue' if river == 'Bayankol' else 'green', icon='info-sign')
    ).add_to(m)

# Схематичное обозначение русел (линии между точками для демонстрации)
river_lines = [
    # Bayankol line (approx)
    [[44.6, 79.0], [44.5, 79.2], [44.4, 79.5]],
    # Lepsy line (approx)
    [[44.4, 78.3], [44.2, 78.5], [44.1, 78.7]]
]

for line in river_lines:
    folium.PolyLine(line, color="blue", weight=3, opacity=0.8).add_to(m)

# Сохранение карты
m.save("155.html")

print("\nРезультаты сохранены: график 'flood_dynamics.png' и карта '155.html'")