import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from scipy import stats
import matplotlib.pyplot as plt

# 1. Генерация синтетических данных (имитация реальных данных по реке Бызж)
# Предположим, мы имеем 50 сельскохозяйственных участков вдоль реки
np.random.seed(42)
n_plots = 50

# Координаты в районе бассейна реки Бызж (примерные координаты)
base_lat, base_lon = 43.5, 40.2 
lats = base_lat + np.random.uniform(-0.1, 0.1, n_plots)
lons = base_lon + np.random.uniform(-0.1, 0.1, n_plots)

# Объем потребления воды (м3 на гектар)
water_consumption = np.random.normal(5000, 1500, n_plots)
water_consumption = np.clip(water_consumption, 1000, 10000)

# Урожайность (ц/га) с добавлением зависимости от воды + случайный шум
# Урожайность = 2.0 * (вода/1000) + шум
crop_yield = 2.0 * (water_consumption / 1000) + np.random.normal(10, 3, n_plots)

df = pd.DataFrame({
    'plot_id': range(1, n_plots + 1),
    'lat': lats,
    'lon': lons,
    'water_vol': water_consumption,
    'yield_val': crop_yield
})

# 2. Статистический анализ корреляции
correlation, p_value = stats.pearsonr(df['water_vol'], df['yield_val'])
print(f"Коэффициент корреляции Пирсона: {correlation:.4f}")
print(f"P-value: {p_value:.4f}")

# 3. Визуализация данных на карте
# Создаем карту, центрированную в районе исследования
m = folium.Map(location=[base_lat, base_lon], zoom_start=11, tiles='OpenStreetMap')

# Функция для определения цвета в зависимости от урожайности
def get_color(yield_val):
    if yield_val > 25:
        return 'green'
    elif yield_val > 15:
        return 'yellow'
    else:
        return 'red'

# Добавление участков на карту
for idx, row in df.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=7,
        popup=f"Участок {row['plot_id']}<br>Вода: {row['water_vol']:.1f} м3<br>Урожай: {row['yield_val']:.1f} ц/га",
        color=get_color(row['yield_val']),
        fill=True,
        fill_color=get_color(row['yield_val']),
        fill_opacity=0.7
    ).add_to(m)

# Добавление легенды (текстовое описание в HTML)
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 160px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Урожайность:</b><br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Высокая (>25)<br>
     <i style="background:yellow; width:10px; height:10px; display:inline-block"></i> Средняя (15-25)<br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> Низкая (<15)
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение карты
m.save("185.html")

# 4. Дополнительный график корреляции (сохраняется локально)
plt.figure(figsize=(8, 6))
plt.scatter(df['water_vol'], df['yield_val'], color='blue', alpha=0.6)
plt.title(f"Корреляция: Потребление воды vs Урожайность\n(r = {correlation:.2f})")
plt.xlabel("Объем потребления воды (м3/га)")
plt.ylabel("Урожайность (ц/га)")
plt.grid(True)
plt.savefig("correlation_plot.png")

print("Анализ завершен. Карта сохранена в '185.html', график в 'correlation_plot.png'.")