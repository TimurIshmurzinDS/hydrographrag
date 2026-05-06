import pandas as pd
import numpy as np
import folium

# 1. Создание синтетического набора данных по стоку рек (м3/с или млн м3)
# В реальном сценарии здесь будет загрузка CSV или подключение к API гидропоста
np.random.seed(42)
years = np.arange(2000, 2021)
lepsy_discharge = np.random.randint(15, 50, size=len(years))
tekes_discharge = np.random.randint(10, 40, size=len(years))

df = pd.DataFrame({
    'Year': years,
    'Lepsy_River': lepsy_discharge,
    'Tekes_River': tekes_discharge
})

# 2. Поиск года с самым высоким уровнем стока в реке Lepsy
max_lepsy_row = df.loc[df['Lepsy_River'].idxmax()]
max_year = int(max_lepsy_row['Year'])
max_lepsy_val = max_lepsy_row['Lepsy_River']

# 3. Сравнение с аналогичным периодом в реке Tekes
tekes_val_same_year = df.loc[df['Year'] == max_year, 'Tekes_River'].values[0]
difference = max_lepsy_val - tekes_val_same_year

print(f"Год с максимальным стоком реки Лепсы: {max_year}")
print(f"Сток Лепсы в этот год: {max_lepsy_val}")
print(f"Сток Текес в этот год: {tekes_val_same_year}")
print(f"Разница: {difference}")

# 4. Геопространственная визуализация
# Примерные координаты рек в Восточном Казахстане
coords = {
    'Lepsy': [49.5, 84.5], 
    'Tekes': [49.2, 85.2]
}

# Создание карты
m = folium.Map(location=[49.3, 84.8], zoom_start=7, tiles='OpenStreetMap')

# Добавление маркера для реки Лепсы
folium.Marker(
    location=coords['Lepsy'],
    popup=f"Река Лепсы\nМакс. сток: {max_lepsy_val} в {max_year} г.",
    tooltip="Lepsy River",
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# Добавление маркера для реки Текес
folium.Marker(
    location=coords['Tekes'],
    popup=f"Река Текес\nСток в {max_year} г.: {tekes_val_same_year}",
    tooltip="Tekes River",
    icon=folium.Icon(color='green', icon='info-sign')
).add_to(m)

# Добавление текстового пояснения на карту через всплывающее окно в центре
info_text = f"Анализ: В {max_year} году река Лепсы достигла пика ({max_lepsy_val}). " \
            f"В этот же период сток реки Текес составил {tekes_val_same_year}. " \
            f"Разница: {difference} ед."

# Создаем небольшую точку-инфо в центре
folium.Marker(
    location=[49.35, 84.85],
    popup=folium.Popup(info_text, max_width=300),
    icon=folium.Icon(color='red', icon='star')
).add_to(m)

# Сохранение карты
m.save("132.html")

print("Карта успешно сохранена в файл 132.html")