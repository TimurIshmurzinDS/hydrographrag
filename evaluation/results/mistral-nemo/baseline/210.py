import pandas as pd
import folium

# 1. Подготовка данных
lepsy_data = pd.read_csv('lespy_river_discharge.csv')
aksu_data = pd.read_csv('aksu_river_discharge.csv')

# 2. Преобразование данных
lepsy_monthly_avg = lepsy_data.groupby(pd.Grouper(key='date', freq='M')).mean()['discharge']
aksu_monthly_avg = aksu_data.groupby(pd.Grouper(key='date', freq='M')).mean()['discharge']

# 3. Анализ данных (в данном примере мы просто выведем средний ежемесячный сток)
print("Lepsy River monthly average discharge:")
print(lespy_monthly_avg)

print("\nAksu River monthly average discharge:")
print(aksu_monthly_avg)

# 4. Визуализация результатов
m = folium.Map(location=[50, 30], zoom_start=4) # примерные координаты и масштаб

folium.Marker([lepsy_data['latitude'].mean(), lespy_data['longitude'].mean()], popup='Lepsy River').add_to(m)
folium.Marker([aksu_data['latitude'].mean(), aksu_data['longitude'].mean()], popup='Aksu River').add_to(m)

# Сохранение карты
m.save("210.html")