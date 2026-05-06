import pandas as pd
import numpy as np
from scipy.stats import norm, poisson
import folium

# Шаг 1: Сбор данных (примерные данные)
data = {
    'date': pd.date_range(start='2010-01-01', periods=365*10, freq='D'),
    'ili_water_level': np.random.normal(loc=100, scale=10, size=365*10),
    'shynzhaly_water_level': np.random.normal(loc=80, scale=8, size=365*10)
}
df = pd.DataFrame(data)

# Шаг 2: Предварительная обработка данных
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Определение порога экстремальных паводков (например, уровень воды выше среднего на 3 стандартных отклонения)
ili_threshold = df['ili_water_level'].mean() + 3 * df['ili_water_level'].std()
shynzhaly_threshold = df['shynzhaly_water_level'].mean() + 3 * df['shynzhaly_water_level'].std()

# Шаг 3: Анализ временных рядов
df['ili_extreme'] = df['ili_water_level'] > ili_threshold
df['shynzhaly_extreme'] = df['shynzhaly_water_level'] > shynzhaly_threshold

# Шаг 4: Статистический анализ
ili_extreme_count = df['ili_extreme'].sum()
shynzhaly_extreme_count = df['shynzhaly_extreme'].sum()

total_days = len(df)
ili_probability = ili_extreme_count / total_days
shynzhaly_probability = shynzhaly_extreme_count / total_days

print(f"Вероятность экстремальных паводков на реке Или: {ili_probability:.4f}")
print(f"Вероятность экстремальных паводков на реке Шынжалы: {shynzhaly_probability:.4f}")

# Шаг 5: Геоспатиальная модель (примерные координаты)
ili_coords = [43.2186, 76.9061]  # примерные координаты реки Или
shynzhaly_coords = [43.1544, 76.8961]  # примерные координаты реки Шынжалы

# Шаг 6: Визуализация результатов
m = folium.Map(location=[43.1865, 76.8961], zoom_start=10)

folium.Marker(
    location=ili_coords,
    popup=f"Вероятность экстремальных паводков: {ili_probability:.2%}",
    icon=folium.Icon(color='red')
).add_to(m)

folium.Marker(
    location=shynzhaly_coords,
    popup=f"Вероятность экстремальных паводков: {shynzhaly_probability:.2%}",
    icon=folium.Icon(color='blue')
).add_to(m)

m.save("164.html")