import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium

# 1. Генерация синтетических исторических данных
# Имитируем режим рек с снеговым питанием (пик в мае-июне)
def generate_river_data(river_name, base_flow, peak_flow, shift=5):
    months = np.arange(1, 13)
    # Создаем синусоидальную кривую для имитации сезонности
    seasonal_pattern = (np.sin((months - shift) * (2 * np.pi / 12)) + 1) / 2
    flow = base_flow + (peak_flow - base_flow) * seasonal_pattern
    # Добавляем случайный шум для реалистичности
    noise = np.random.normal(0, (peak_flow - base_flow) * 0.05, 12)
    return flow + noise

np.random.seed(42)
months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']

# Данные для Shilik River (условно более стабильный сток)
shilik_flow = generate_river_data("Shilik", base_flow=10, peak_flow=45)
# Данные для Kishi Almaty River (более выраженная сезонность/паводки)
kishi_almaty_flow = generate_river_data("Kishi Almaty", base_flow=5, peak_flow=60)

df = pd.DataFrame({
    'Month': months,
    'Shilik_River': shilik_flow,
    'Kishi_Almaty_River': kishi_almaty_flow
})

# 2. Статистический анализ
stats = {
    'River': ['Shilik', 'Kishi Almaty'],
    'Mean': [df['Shilik_River'].mean(), df['Kishi_Almaty_River'].mean()],
    'Max': [df['Shilik_River'].max(), df['Kishi_Almaty_River'].max()],
    'Min': [df['Shilik_River'].min(), df['Kishi_Almaty_River'].min()],
    'CV': [df['Shilik_River'].std() / df['Shilik_River'].mean(), 
           df['Kishi_Almaty_River'].std() / df['Kishi_Almaty_River'].mean()]
}
df_stats = pd.DataFrame(stats)

print("Статистические показатели стока:")
print(df_stats)

# 3. Визуализация гидрографа
plt.figure(figsize=(12, 6))
plt.plot(df['Month'], df['Shilik_River'], marker='o', label='Shilik River', color='blue', linewidth=2)
plt.plot(df['Month'], df['Kishi_Almaty_River'], marker='s', label='Kishi Almaty River', color='green', linewidth=2)
plt.title('Сравнение сезонной изменчивости стока рек', fontsize=14)
plt.xlabel('Месяц', fontsize=12)
plt.ylabel('Расход воды (м³/с)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.savefig("runoff_comparison.png")
plt.show()

# 4. Геопространственная визуализация (Folium)
# Приблизительные координаты рек
locations = {
    "Shilik River": [43.5, 80.1], 
    "Kishi Almaty River": [43.2, 77.0]
}

m = folium.Map(location=[43.3, 78.5], zoom_start=6, tiles='OpenStreetMap')

for river, coords in locations.items():
    folium.Marker(
        location=coords,
        popup=f"{river}: Сток {df_stats.loc[df_stats['River']==river, 'Mean'].values[0]:.2f} м³/с",
        icon=folium.Icon(color='blue' if 'Shilik' in river else 'green', icon='info-sign')
    ).add_to(m)

# Сохранение карты строго в файл 126.html
m.save("126.html")

print("\nАнализ завершен. Карта сохранена в файл 126.html, график в runoff_comparison.png")