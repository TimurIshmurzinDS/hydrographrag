import pandas as pd
import folium
from folium.plugins import HeatMap

# Пример данных о стоимости жилья в крупных городах за разные периоды времени
data = {
    'City': ['Москва', 'Санкт-Петербург', 'Новосибирск'],
    'Year': [1900, 1950, 2000],
    'Cost': [300, 400, 800]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Преобразование данных для визуализации на карте
m = folium.Map(location=[55.755826, 37.6173], zoom_start=4)

# Добавление точек на карте с информацией о стоимости жилья
for index, row in df.iterrows():
    folium.Marker(
        location=[55.755826, 37.6173],  # Пример координат для каждого города (замените на реальные)
        popup=f"Город: {row['City']}, Год: {row['Year']}, Стоимость: {row['Cost']} руб.",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("280.html")