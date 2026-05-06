import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from folium import plugins

# 1. Генерация синтетических исторических данных
# Имитируем данные за 10 лет (120 месяцев) для двух рек
np.random.seed(42)
months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 
          'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
years = range(2013, 2023)

# Базовые профили сезонности (типичный снего-ледниковый режим)
# Lepsy: более выраженный весенний пик
lepsy_profile = [10, 12, 25, 60, 110, 150, 140, 120, 70, 40, 20, 15]
# Aksu: более растянутый летний сток (ледниковое питание)
aksu_profile = [15, 18, 30, 50, 90, 130, 160, 150, 100, 60, 30, 20]

data_list = []
for year in years:
    for i, month in enumerate(months):
        # Добавляем случайный шум к базовому профилю
        lepsy_val = lepsy_profile[i] + np.random.normal(0, lepsy_profile[i]*0.2)
        aksu_val = aksu_profile[i] + np.random.normal(0, aksu_profile[i]*0.2)
        data_list.append({'Year': year, 'Month': month, 'Month_Idx': i+1, 
                          'Lepsy': max(0, lepsy_val), 'Aksu': max(0, aksu_val)})

df = pd.DataFrame(data_list)

# 2. Расчет средних многолетних значений
seasonal_avg = df.groupby('Month_Idx').mean(numeric_only=True).reindex(range(1, 13))
seasonal_avg['Month'] = months

# 3. Визуализация сезонного распределения (График)
plt.figure(figsize=(12, 6))
plt.plot(months, seasonal_avg['Lepsy'], marker='o', label='Lepsy River', color='blue', linewidth=2)
plt.plot(months, seasonal_avg['Aksu'], marker='s', label='Aksu River', color='green', linewidth=2)
plt.title('Сравнительный анализ сезонного распределения стока рек', fontsize=14)
plt.xlabel('Месяц', fontsize=12)
plt.ylabel('Средний расход воды (м³/с)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.savefig("runoff_analysis.png")
plt.close()

# 4. Геопространственная визуализация
# Приблизительные координаты рек в Казахстане (регион Жетысу)
locations = {
    "Lepsy River": [43.5, 79.5, seasonal_avg['Lepsy'].mean()],
    "Aksu River": [43.8, 78.5, seasonal_avg['Aksu'].mean()]
}

# Создание карты
m = folium.Map(location=[43.6, 79.0], zoom_start=7, tiles='OpenStreetMap')

for river, info in locations.items():
    folium.Marker(
        location=[info[0], info[1]],
        popup=f"<b>{river}</b><br>Средний расход: {info[2]:.2f} м³/с",
        tooltip=river,
        icon=folium.Icon(color='blue' if 'Lepsy' in river else 'green', icon='info-sign')
    ).add_to(m)

# Добавление линии, имитирующей направление рек (упрощенно)
folium.PolyLine(
    locations=[[43.5, 79.5], [43.2, 79.8]], 
    color='blue', weight=4, opacity=0.8, tooltip='Lepsy River Course'
).add_to(m)

folium.PolyLine(
    locations=[[43.8, 78.5], [43.5, 78.2]], 
    color='green', weight=4, opacity=0.8, tooltip='Aksu River Course'
).add_to(m)

# Сохранение карты
m.save("210.html")

print("Анализ завершен. График сохранен в 'runoff_analysis.png', карта в '210.html'.")