import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import folium
from datetime import datetime, timedelta

# =============================================================================
# 1. Генерация синтетических данных (имитация данных гидропоста и метеостанции)
# =============================================================================
np.random.seed(42)
date_rng = pd.date_range(start='2018-01-01', end='2023-12-31', freq='D')
n_days = len(date_rng)

# Имитация сезонности осадков (синусоида + шум)
# Предположим, что пик осадков приходится на лето
precipitation = 5 + 10 * np.sin(2 * np.pi * date_rng.dayofyear / 365.25) + np.random.normal(0, 3, n_days)
precipitation = np.clip(precipitation, 0, None) # Осадки не могут быть отрицательными

# Имитация уровня воды: базовый сток + влияние осадков с лагом в 3 дня + шум
water_level = np.zeros(n_days)
base_flow = 2.0
lag = 3
for i in range(lag, n_days):
    # Уровень воды зависит от осадков за последние несколько дней
    water_level[i] = base_flow + 0.15 * np.sum(precipitation[i-lag:i]) + np.random.normal(0, 0.2)

df = pd.DataFrame({'date': date_rng, 'precipitation': precipitation, 'water_level': water_level})
df.set_index('date', inplace=True)

# =============================================================================
# 2. Анализ влияния (Корреляция и Регрессия)
# =============================================================================

# Сдвиг данных для учета лага (Lagging)
df['precip_lagged'] = df['precipitation'].shift(lag)
df_clean = df.dropna()

# Расчет корреляции Пирсона
correlation, p_value = stats.pearsonr(df_clean['precip_lagged'], df_clean['water_level'])

# Линейная регрессия
slope, intercept, r_value, p_val, std_err = stats.linregress(df_clean['precip_lagged'], df_clean['water_level'])

print(f"Correlation Coefficient: {correlation:.3f}")
print(f"P-value: {p_value:.5f}")
print(f"Regression Equation: Water Level = {intercept:.3f} + {slope:.3f} * Precip_Lagged")

# =============================================================================
# 3. Визуализация результатов
# =============================================================================
plt.figure(figsize=(15, 10))

# График временных рядов
plt.subplot(2, 1, 1)
plt.plot(df.index, df['precipitation'], color='blue', label='Precipitation (mm)', alpha=0.6)
plt.ylabel('Precipitation (mm)')
plt.legend(loc='upper left')
plt.twinx()
plt.plot(df.index, df['water_level'], color='green', label='Water Level (m)', alpha=0.8)
plt.ylabel('Water Level (m)')
plt.legend(loc='upper right')
plt.title('Karkara River: Precipitation vs Water Level (2018-2023)')

# Диаграмма рассеяния с линией регрессии
plt.subplot(2, 1, 2)
sns.regplot(x='precip_lagged', y='water_level', data=df_clean, 
            scatter_kws={'alpha':0.3, 'color':'gray'}, line_kws={'color':'red'})
plt.xlabel('Lagged Precipitation (mm)')
plt.ylabel('Water Level (m)')
plt.title(f'Influence Analysis (Correlation: {correlation:.2f})')

plt.tight_layout()
plt.savefig("analysis_plot.png")
plt.show()

# =============================================================================
# 4. Геопространственная визуализация (Folium)
# =============================================================================

# Координаты реки Karkara (примерные координаты для демонстрации)
# В реальности здесь должны быть точные координаты створа наблюдения
karkara_coords = [10.5, 39.5] 

m = folium.Map(location=karkara_coords, zoom_start=8, tiles='OpenStreetMap')

# Добавление маркера станции мониторинга
folium.Marker(
    location=karkara_coords,
    popup=f"Karkara River Station\nCorr: {correlation:.2f}",
    tooltip="Monitoring Station",
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# Имитация зоны водосбора (окружность вокруг станции)
folium.Circle(
    location=karkara_coords,
    radius=50000, # 50 км
    color='blue',
    fill=True,
    fill_color='blue',
    fill_opacity=0.2,
    popup='Approximate Catchment Area'
).add_to(m)

# Сохранение карты
m.save("60.html")
print("Map has been saved as 60.html")