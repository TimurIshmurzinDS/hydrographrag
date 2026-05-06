import pandas as pd
import folium

# Загрузка данных (пример)
data = {
    'Река': ['Tentek River', 'Sharyn River', 'Tentek River', 'Sharyn River'],
    'Статус': ['Передается', 'Не передается', 'Передается', 'Передается'],
    'Дата': ['2023-10-26', '2023-10-25', '2023-10-27', '2023-10-28']
}

df = pd.DataFrame(data)

# Сравнение статусов
status_comparison = df.groupby('Река')['Статус'].unique()

print("Сравнение статусов передачи данных:")
print(status_comparison)

# Визуализация (необязательно)
m = folium.Map(location=[42.5, 78], zoom_start=6)

for index, row in df.iterrows():
    folium.Marker(location=[row['Река'], 42.5], popup=f"Статус: {row['Статус']}").add_to(m)

m.save("75.html")