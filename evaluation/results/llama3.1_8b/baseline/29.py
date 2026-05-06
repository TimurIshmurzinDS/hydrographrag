import pandas as pd
import folium

# Загрузите данные о расходе воды для реки Uzyn Kargaly River
data = {
    'Дата': ['2022-03-01', '2022-03-15', '2022-04-01'],
    'Расход воды (м³/с)': [10, 20, 30]
}
df = pd.DataFrame(data)

# Определите значения расхода воды во время весеннего паводка
pavodok_period = df[(df['Дата'] >= '2022-03-01') & (df['Дата'] <= '2022-04-15')]
pavodok_values = pavodok_period['Расход воды (м³/с)'].unique()

# Создайте карту с помощью библиотеки folium
m = folium.Map(location=[43.5, 79], zoom_start=10)

# Добавьте на карту значения расхода воды во время весеннего паводка
for value in pavodok_values:
    folium.Marker([43.5, 79], popup=f'Расход воды: {value} м³/с').add_to(m)

# Сохраните карту в файл
m.save("29.html")