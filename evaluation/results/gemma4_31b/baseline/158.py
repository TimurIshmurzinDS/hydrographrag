import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster
import datetime

# 1. Симуляция гидрологических данных (так как реальные данные закрыты)
# Создаем синтетический набор данных за 5 лет для двух рек
def generate_river_data(river_name):
    np.random.seed(42 if river_name == "Bayankol" else 7)
    dates = pd.date_range(start="2019-01-01", end="2023-12-31", freq='D')
    
    # Моделируем сезонность: пик в марте-мае (весенний паводок)
    # Используем синусоиду с добавлением случайного шума и экстремальных пиков
    day_of_year = dates.dayofyear
    seasonal_pattern = 2 * np.sin(2 * np.pi * (day_of_year - 100) / 365) + 5
    noise = np.random.normal(0, 0.5, len(dates))
    
    # Добавляем случайные экстремальные паводки в разные годы
    extreme_events = np.zeros(len(dates))
    for year in range(2019, 2024):
        start_day = np.random.randint(70, 120) # Март-Апрель
        duration = np.random.randint(5, 15)
        extreme_events[year*365 + start_day : year*365 + start_day + duration] += np.random.uniform(3, 6)
        
    water_levels = seasonal_pattern + noise + extreme_events
    return pd.DataFrame({'date': dates, 'level': water_levels, 'river': river_name})

# Сбор данных
df_bayankol = generate_river_data("Bayankol")
df_sarykan = generate_river_data("Sarykan")
df = pd.concat([df_bayankol, df_sarykan])

# 2. Анализ опасных периодов
def analyze_danger_periods(df_river):
    # Определяем порог опасности (Среднее + 2 сигмы)
    threshold = df_river['level'].mean() + 2 * df_river['level'].std()
    
    # Помечаем опасные дни
    df_river['is_dangerous'] = df_river['level'] > threshold
    
    # Группируем по месяцам, чтобы найти наиболее опасный период
    df_river['month'] = df_river['date'].dt.month
    monthly_risk = df_river.groupby('month')['is_dangerous'].mean().sort_values(ascending=False)
    
    return monthly_risk, threshold

risk_bayankol, thresh_b = analyze_danger_periods(df_bayankol)
risk_sarykan, thresh_s = analyze_danger_periods(df_sarykan)

print(f"Наиболее опасные месяцы для Bayankol:\n{risk_bayankol.head(3)}")
print(f"Наиболее опасные месяцы для Sarykan:\n{risk_sarykan.head(3)}")

# 3. Визуализация на карте
# Координаты (приблизительные для региона)
coords_bayankol = [[46.5, 66.2], [46.6, 66.4], [46.7, 66.5]] 
coords_sarykan = [[46.8, 66.8], [46.9, 67.0], [47.0, 67.1]]

# Создание карты
m = folium.Map(location=[46.7, 66.5], zoom_start=7, tiles='CartoDB positron')

# Стилизация рек
def add_river_to_map(coords, name, color, risk_months):
    # Рисуем русло
    folium.PolyLine(coords, color=color, weight=5, opacity=0.8, tooltip=f"River: {name}").add_to(m)
    
    # Добавляем маркеры опасности в ключевых точках
    for i, coord in enumerate(coords):
        folium.CircleMarker(
            location=coord,
            radius=10,
            color='red',
            fill=True,
            fill_color='yellow',
            popup=f"River {name}: High risk in months {risk_months}"
        ).add_to(m)

# Определяем самые опасные месяцы (индексы месяцев)
top_months_b = risk_bayankol.index[0:2].tolist()
top_months_s = risk_sarykan.index[0:2].tolist()

add_river_to_map(coords_bayankol, "Bayankol", "blue", top_months_b)
add_river_to_map(coords_sarykan, "Sarykan", "green", top_months_s)

# Добавление легенды через HTML
legend_html = f'''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 200px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Легенда паводков:</b><br>
     Синяя линия: Bayankol (Риск: {top_months_b})<br>
     Зеленая линия: Sarykan (Риск: {top_months_s})<br>
     Желтые точки: Зоны высокого риска
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение карты
m.save("158.html")
print("Map has been saved as 158.html")