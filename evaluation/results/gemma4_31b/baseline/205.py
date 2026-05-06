import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from scipy import stats
from datetime import datetime, timedelta

# =============================================================================
# 1. Симуляция данных (так как реальные данные реки Лепсы являются закрытыми)
# =============================================================================
np.random.seed(42)
years = np.arange(2000, 2024)
n_years = len(years)

# Симулируем дату начала снеготаяния (в днях от 1 января)
# Обычно снеготаяние начинается с конца марта по май (дни 80-120)
snowmelt_start_days = np.random.randint(80, 120, size=n_years)

# Симулируем пиковый расход воды (м3/с)
# Предположим, что более раннее таяние при определенном объеме снега ведет к более резким пикам
# Q_max = базовый_сток + влияние_даты + шум
q_max = 50 + (120 - snowmelt_start_days) * 0.5 + np.random.normal(0, 5, n_years)

df = pd.DataFrame({
    'Year': years,
    'Snowmelt_Start_Day': snowmelt_start_days,
    'Peak_Discharge': q_max
})

# =============================================================================
# 2. Статистический анализ
# =============================================================================
# Корреляция между датой начала таяния и пиковым стоком
correlation, p_value = stats.pearsonr(df['Snowmelt_Start_Day'], df['Peak_Discharge'])

# Линейная регрессия
slope, intercept, r_value, p_val, std_err = stats.linregress(df['Snowmelt_Start_Day'], df['Peak_Discharge'])

print(f"Correlation coefficient: {correlation:.3f}")
print(f"P-value: {p_value:.3f}")
print(f"Regression Equation: Q_max = {intercept:.2f} + {slope:.2f} * Day")

# =============================================================================
# 3. Визуализация графиков
# =============================================================================
plt.figure(figsize=(12, 5))

# График 1: Временные ряды
plt.subplot(1, 2, 1)
plt.plot(df['Year'], df['Snowmelt_Start_Day'], color='blue', marker='o', label='День начала таяния')
plt.xlabel('Год')
plt.ylabel('День года')
plt.title('Динамика сроков снеготаяния')
plt.grid(True)
plt.legend()

# График 2: Зависимость стока от даты
plt.subplot(1, 2, 2)
sns.regplot(x='Snowmelt_Start_Day', y='Peak_Discharge', data=df, color='green')
plt.xlabel('День начала снеготаяния')
plt.ylabel('Пиковый расход (м3/с)')
plt.title('Влияние сроков таяния на пик стока')
plt.grid(True)

plt.tight_layout()
plt.savefig("analysis_results.png")
plt.show()

# =============================================================================
# 4. Геопространственная визуализация (Folium)
# =============================================================================
# Координаты реки Лепсы (примерные координаты бассейна в Восточном Казахстане)
lepsy_coords = [48.5, 84.5] 

# Создание карты
m = folium.Map(location=lepsy_coords, zoom_start=8, tiles='OpenStreetMap')

# Добавление имитации гидропостов
stations = [
    {"name": "Station Upper Lepsy", "loc": [48.8, 84.2], "q_avg": 45},
    {"name": "Station Middle Lepsy", "loc": [48.5, 84.6], "q_avg": 70},
    {"name": "Station Lower Lepsy", "loc": [48.2, 85.0], "q_avg": 110},
]

for st in stations:
    folium.CircleMarker(
        location=st["loc"],
        radius=8,
        popup=f"{st['name']}<br>Avg Peak Flow: {st['q_avg']} m3/s",
        color="blue",
        fill=True,
        fill_color="blue"
    ).add_to(m)

# Добавление линии, имитирующей русло реки
river_path = [
    [48.9, 84.1], [48.7, 84.3], [48.5, 84.6], [48.3, 84.8], [48.1, 85.1]
]
folium.PolyLine(river_path, color="blue", weight=4, opacity=0.8, tooltip="Lepsy River").add_to(m)

# Сохранение карты
m.save("205.html")

print("Analysis complete. Map saved as 205.html and plots saved as analysis_results.png")