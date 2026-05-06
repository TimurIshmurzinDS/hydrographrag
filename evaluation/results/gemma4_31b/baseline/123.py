import numpy as np
import pandas as pd
import folium
from scipy import stats
from sklearn.preprocessing import StandardScaler

# -----------------------------------------------------------------------------
# 1. Симуляция данных (так как реальные данные стока требуют доступа к БД)
# -----------------------------------------------------------------------------
def generate_river_data():
    np.random.seed(42)
    time = np.arange(100)
    
    # Исторический паттерн реки Sharyn (синусоида + тренд + шум)
    sharyn_historical = 50 + 20 * np.sin(time / 5) + 0.1 * time + np.random.normal(0, 5, 100)
    
    # Текущий тренд реки Kurty (похожий паттерн, но с небольшим сдвигом и шумом)
    kurty_current = 30 + 15 * np.sin((time - 2) / 5) + 0.12 * time + np.random.normal(0, 5, 100)
    
    return time, sharyn_historical, kurty_current

time, sharyn_data, kurty_data = generate_river_data()

# -----------------------------------------------------------------------------
# 2. Анализ сходства паттернов
# -----------------------------------------------------------------------------
def analyze_trends(data1, data2):
    # Нормализация данных (Z-score), чтобы сравнивать форму, а не амплитуду
    scaler = StandardScaler()
    s1_norm = scaler.fit_transform(data1.reshape(-1, 1)).flatten()
    s2_norm = scaler.fit_transform(data2.reshape(-1, 1)).flatten()
    
    # 1. Коэффициент корреляции Пирсона
    correlation, p_value = stats.pearsonr(s1_norm, s2_norm)
    
    # 2. Сравнение наклонов (линейный тренд)
    slope1, _, _, _, _ = stats.linregress(np.arange(len(s1_norm)), s1_norm)
    slope2, _, _, _, _ = stats.linregress(np.arange(len(s2_norm)), s2_norm)
    
    return correlation, p_value, slope1, slope2

corr, p, slope_sh, slope_ku = analyze_trends(sharyn_data, kurty_data)

# Определение результата
is_matching = "Да" if corr > 0.7 else "Нет"
result_text = f"Результат: Совпадает ли тренд? {is_matching} (Корреляция: {corr:.2f}, p-value: {p:.4f})"
print(result_text)

# -----------------------------------------------------------------------------
# 3. Геопространственная визуализация
# -----------------------------------------------------------------------------
def create_map():
    # Координаты (приблизительные для демонстрации региона Казахстана)
    # Sharyn River area, Kurty River area
    locations = {
        "Sharyn River": [43.5, 79.5],
        "Kurty River": [43.8, 79.2]
    }
    
    # Создание карты
    m = folium.Map(location=[43.6, 79.3], zoom_start=8, tiles='OpenStreetMap')
    
    # Добавление маркеров
    for river, coords in locations.items():
        folium.Marker(
            location=coords,
            popup=f"{river}",
            icon=folium.Icon(color='blue' if 'Sharyn' in river else 'green')
        ).add_to(m)
    
    # Добавление линии между ними для визуализации связи
    folium.PolyLine(
        locations=list(locations.values()),
        color="red",
        weight=2.5,
        opacity=0.8,
        tooltip="Сравниваемый гидрологический регион"
    ).add_to(m)
    
    # Добавление текстового вывода на карту через всплывающее окно в центре
    folium.Popup(result_text).add_to(m)
    
    # Сохранение карты
    m.save("123.html")
    print("Карта сохранена как 123.html")

create_map()