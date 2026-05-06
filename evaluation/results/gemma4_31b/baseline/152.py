import pandas as pd
import numpy as np
import folium
import matplotlib.pyplot as plt

def simulate_seasonal_runoff(river_name, area_km2, avg_annual_precip):
    """
    Симуляция сезонного стока на основе типичного гидрологического режима 
    Восточного Казахстана (снеговое питание).
    """
    months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 
              'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дека']
    
    # Распределение осадков по месяцам (условное)
    precip_dist = np.array([0.06, 0.05, 0.07, 0.08, 0.10, 0.12, 
                            0.11, 0.09, 0.07, 0.06, 0.05, 0.04])
    
    # Коэффициент стока (учитывает снеготаяние и испарение)
    # Весна (Март-Май) имеет самый высокий коэффициент из-за таяния снегов
    runoff_coeff = np.array([0.1, 0.1, 0.4, 0.7, 0.6, 0.3, 
                            0.2, 0.2, 0.2, 0.1, 0.1, 0.1])
    
    monthly_precip = avg_annual_precip * precip_dist
    # Сток = Осадки * Коэффициент * Площадь (упрощенно)
    # Результат в тыс. м3
    monthly_runoff = (monthly_precip * runoff_coeff * area_km2) / 1000 
    
    return pd.DataFrame({'Month': months, 'Runoff': monthly_runoff})

# 1. Параметры рек (приблизительные данные для моделирования)
rivers_data = {
    'Lepsy River': {'coords': [48.5, 84.5], 'area': 12000, 'precip': 550},
    'Shilik River': {'coords': [48.2, 86.0], 'area': 15000, 'precip': 600}
}

# 2. Расчет стока
results = {}
for name, params in rivers_data.items():
    results[name] = simulate_seasonal_runoff(name, params['area'], params['precip'])

# 3. Визуализация графиков стока
plt.figure(figsize=(10, 6))
for name, df in results.items():
    plt.plot(df['Month'], df['Runoff'], marker='o', label=name)

plt.title('Сезонный сток рек Лепсы и Шилик (Модель)')
plt.xlabel('Месяц')
plt.ylabel('Объем стока (условные ед.)')
plt.legend()
plt.grid(True)
plt.savefig("runoff_chart.png")
plt.close()

# 4. Создание карты с помощью folium
# Центр карты в районе Восточного Казахстана
m = folium.Map(location=[48.3, 85.2], zoom_start=7, tiles='OpenStreetMap')

for name, params in rivers_data.items():
    # Добавляем маркеры для рек
    folium.Marker(
        location=params['coords'],
        popup=f"{name}\nПлощадь бассейна: {params['area']} км2",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)
    
    # Имитация русла реки простым кругом (для визуализации зоны влияния)
    folium.Circle(
        location=params['coords'],
        radius=params['area'] * 10, # Масштабирование для визуализации
        color='blue',
        fill=True,
        fill_opacity=0.3,
        popup=f"Бассейн {name}"
    ).add_to(m)

# Сохранение карты
m.save("152.html")

print("Моделирование завершено. Результаты сохранены в '152.html' и 'runoff_chart.png'.")