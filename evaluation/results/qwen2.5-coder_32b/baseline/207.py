import pandas as pd
import numpy as np
from scipy.stats import zscore
import folium
import matplotlib.pyplot as plt

# Предполагаемые данные для примера (в реальности нужно загрузить реальные временные ряды)
data = {
    'date': pd.date_range(start='2003-01-01', end='2023-12-31'),
    'Emel_River_Level': np.random.normal(loc=5, scale=1.5, size=7305),
    'Turgen_River_Level': np.random.normal(loc=4.5, scale=1.2, size=7305)
}

df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Определение экстремальных значений с помощью Z-оценки
def find_extremes(series):
    z_scores = zscore(series)
    return series[z_scores > 3]  # Предполагаем, что значения выше 3 стандартных отклонений - экстремальные

emel_extremes = df['Emel_River_Level'].resample('Y').apply(find_extremes).dropna()
turgen_extremes = df['Turgen_River_Level'].resample('Y').apply(find_extremes).dropna()

# Подсчет количества экстремальных событий за каждый год
emel_extreme_counts = emel_extremes.apply(lambda x: len(x))
turgen_extreme_counts = turgen_extremes.apply(lambda x: len(x))

# Визуализация данных на графике
plt.figure(figsize=(14, 7))
plt.plot(emel_extreme_counts.index.year, emel_extreme_counts.values, label='Emel River', marker='o')
plt.plot(turgen_extreme_counts.index.year, turgen_extreme_counts.values, label='Turgen River', marker='x')
plt.title('Частота экстремальных меженный в реках Emel и Turgen за последние 20 лет')
plt.xlabel('Год')
plt.ylabel('Количество экстремальных событий')
plt.legend()
plt.grid(True)
plt.savefig("extreme_events_comparison.png")
plt.show()

# Создание карты с отметками местоположения рек
m = folium.Map(location=[43.2619, 76.8950], zoom_start=10)  # Координаты примерные

folium.Marker(
    location=[43.2619, 76.8950],
    popup='Emel River',
    icon=folium.Icon(color='blue')
).add_to(m)

folium.Marker(
    location=[43.2222, 76.9556],  # Координаты примерные
    popup='Turgen River',
    icon=folium.Icon(color='green')
).add_to(m)

m.save("207.html")