import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import folium

# Загрузка данных
shilik_data = pd.read_csv('Shilik_River.csv', parse_dates=['date'], index_col='date')
kishi_data = pd.read_csv('Kishi_Almaty_River.csv', parse_dates=['date'], index_col='date')

# Предварительный анализ данных
print("Предварительный анализ данных:")
print(shilik_data.info())
print(kishi_data.info())

# Извлечение сезонных компонентов
shilik_decomposition = seasonal_decompose(shilik_data['flow'], model='additive', period=12)
kishi_decomposition = seasonal_decompose(kishi_data['flow'], model='additive', period=12)

# Визуализация сезонных компонентов
plt.figure(figsize=(14, 8))

plt.subplot(311)
shilik_decomposition.trend.plot(ax=plt.gca())
plt.title('Trend Component of Shilik River')

plt.subplot(312)
shilik_decomposition.seasonal.plot(ax=plt.gca())
plt.title('Seasonal Component of Shilik River')

plt.subplot(313)
shilik_decomposition.resid.plot(ax=plt.gca())
plt.title('Residual Component of Shilik River')

plt.tight_layout()
plt.show()

plt.figure(figsize=(14, 8))

plt.subplot(311)
kishi_decomposition.trend.plot(ax=plt.gca())
plt.title('Trend Component of Kishi Almaty River')

plt.subplot(312)
kishi_decomposition.seasonal.plot(ax=plt.gca())
plt.title('Seasonal Component of Kishi Almaty River')

plt.subplot(313)
kishi_decomposition.resid.plot(ax=plt.gca())
plt.title('Residual Component of Kishi Almaty River')

plt.tight_layout()
plt.show()

# Сравнение сезонных изменчивостей
seasonal_shilik = shilik_decomposition.seasonal
seasonal_kishi = kishi_decomposition.seasonal

comparison_df = pd.DataFrame({'Shilik Seasonal': seasonal_shilik, 'Kishi Almaty Seasonal': seasonal_kishi})
comparison_df.plot(kind='bar', figsize=(14, 6))
plt.title('Comparison of Seasonal Variability')
plt.xlabel('Month')
plt.ylabel('Flow')
plt.show()

# Визуализация на карте
m = folium.Map(location=[52.0937, 85.2708], zoom_start=10)

folium.Marker([52.0937, 85.2708], popup='Shilik River', icon=folium.Icon(color='blue')).add_to(m)
folium.Marker([52.0937, 85.2708], popup='Kishi Almaty River', icon=folium.Icon(color='red')).add_to(m)

m.save("126.html")