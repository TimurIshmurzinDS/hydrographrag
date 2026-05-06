import pandas as pd
from folium import Map, Marker

# Данные о сельскохозяйственных продуктах и соответствующих криптовалютах
data = {
    'Продукт': ['Кукуруза', 'Пшеница', 'Соя'],
    'Криптовалюта': ['BTC', 'ETH', 'LTC']
}

df = pd.DataFrame(data)

# Данные о географическом положении и экономической стабильности
geo_data = {
    'Река': ['Бутак'],
    'Страна': ['Казахстан'],
    'Экономическая стабильность': [0.8]  # на шкале от 0 до 1
}

geo_df = pd.DataFrame(geo_data)

# Объединение данных
merged_df = pd.merge(df, geo_df, on='Река')

# Определение наиболее подходящей криптовалюты
best_crypto = merged_df.loc[merged_df['Экономическая стабильность'].idxmax()]['Криптовалюта']

print(f'Лучшая криптовалюта для инвестиций в сельское хозяйство реки Бутак: {best_crypto}')

# Визуализация на карте
m = Map(location=[46.5, 68.0], zoom_start=6)
Marker(location=[46.5, 68.0], popup='Река Бутак').add_to(m)

for index, row in merged_df.iterrows():
    Marker(location=[row['Экономическая стабильность'] * 10 + 45, row['Криптовалюта'].ord() * 2 - 70],
           popup=f'Продукт: {row["Продукт"]}, Криптовалюта: {row["Криптовалюта"]}').add_to(m)

m.save("268.html")