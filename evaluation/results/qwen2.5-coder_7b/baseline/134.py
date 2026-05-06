import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium

# Пример данных (замените на реальные данные)
data = {
    'Bayankol': [100, 120, 130, 140, 150, 160, 170, 180, 190, 200],
    'Kishi Almaty': [80, 90, 100, 110, 120, 130, 140, 150, 160, 170]
}

# Преобразование данных в DataFrame
df = pd.DataFrame(data)
df['Date'] = pd.date_range(start='2013-01-01', periods=10, freq='Y')
df.set_index('Date', inplace=True)

# Вычисление волатильности (стандартное отклонение)
volatility_bayankol = df['Bayankol'].std()
volatility_kishi_almaty = df['Kishi Almaty'].std()

print(f"Волатильность стока в реке Bayankol River: {volatility_bayankol:.2f}")
print(f"Волатильность стока в реке Kishi Almaty River: {volatility_kishi_almaty:.2f}")

# Визуализация данных
plt.figure(figsize=(10, 5))
plt.plot(df.index, df['Bayankol'], label='Bayankol')
plt.plot(df.index, df['Kishi Almaty'], label='Kishi Almaty')
plt.xlabel('Год')
plt.ylabel('Количество воды')
plt.title('Сравнение количества воды в реках Bayankol и Kishi Almaty')
plt.legend()
plt.show()

# Визуализация на карте (пример)
m = folium.Map(location=[43.21, 76.90], zoom_start=5)

folium.Marker([43.21, 76.90], popup='Bayankol River', icon=folium.Icon(color='blue')).add_to(m)
folium.Marker([43.21, 76.90], popup='Kishi Almaty River', icon=folium.Icon(color='red')).add_to(m)

m.save("134.html")