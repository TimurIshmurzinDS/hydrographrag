import pandas as pd
import folium
from folium.plugins import HeatMap

# Пример данных о расходе воды на реках Koktal и Baskan
data = {
    'date': ['2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01', '2023-05-01', '2023-06-01'],
    'Koktal': [10, 15, 20, 25, 30, 35],
    'Baskan': [8, 12, 17, 22, 27, 32]
}

# Преобразование данных в DataFrame
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

# Анализ сезонных колебаний
koktal_seasonal_mean = df['Koktal'].mean()
baskan_seasonal_mean = df['Baskan'].mean()

# Прогнозирование сезонного затопления (простой пример)
df['Koktal_prediction'] = koktal_seasonal_mean + 2 * (df['date'].dt.month - 1) / 5
df['Baskan_prediction'] = baskan_seasonal_mean + 2 * (df['date'].dt.month - 1) / 5

# Создание карты
m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)

# Добавление теплового слоя для демонстрации риска затопления
heat_data = [
    [40.7128, -74.0060, df['Koktal_prediction'].iloc[i]],
    [40.7128, -74.0060, df['Baskan_prediction'].iloc[i]]
]
HeatMap(heat_data).add_to(m)

# Сохранение карты
m.save("85.html")