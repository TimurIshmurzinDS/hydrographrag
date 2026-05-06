import folium
from geopandas import read_file
import pandas as pd

# Загрузка данных о притоках реки Каскелен
kaskelen_sources = read_file('path_to_kaskelen_sources.shp')

# Пример данных о стоимости оборудования и затратах на электроэнергию (в долларах)
equipment_costs = {
    'GPU': 1000,
    'ASIC': 5000
}

electricity_cost_per_kwh = 0.12

# Пример данных о доходах от биткоин-добывания (в долларах за килобиткоин)
revenue_per_kbtc = 10000

# Создание карты
m = folium.Map(location=[kaskelen_sources.geometry.centroid.y.mean(), kaskelen_sources.geometry.centroid.x.mean()], zoom_start=6)

# Функция для расчета затрат и доходов
def calculate_costs_and_revenue(region, equipment_type):
    # Пример данных о количестве оборудования в регионе (в штуках)
    num_equipment = 10
    
    # Расчет затрат на оборудование
    equipment_cost = num_equipment * equipment_costs[equipment_type]
    
    # Расчет затрат на электроэнергию (пример: 24 часа работы в день, 30 дней в месяц)
    electricity_cost_per_month = region.geometry.area.mean() * 1000 * 24 * 30 * electricity_cost_per_kwh
    
    # Расчет доходов от биткоин-добывания
    revenue_per_month = num_equipment * revenue_per_kbtc
    
    return equipment_cost, electricity_cost_per_month, revenue_per_month

# Пример анализа для каждого притока
for index, row in kaskelen_sources.iterrows():
    region_name = row['name']
    equipment_type = 'GPU'  # Пример выбора оборудования
    
    equipment_cost, electricity_cost, revenue = calculate_costs_and_revenue(row, equipment_type)
    
    print(f"Регион: {region_name}")
    print(f"Тип оборудования: {equipment_type}")
    print(f"Затраты на оборудование: ${equipment_cost:.2f}")
    print(f"Затраты на электроэнергию в месяц: ${electricity_cost:.2f}")
    print(f"Доходы от биткоин-добывания в месяц: ${revenue:.2f}")
    
    # Добавление маркера на карту
    folium.Marker(
        location=[row.geometry.centroid.y, row.geometry.centroid.x],
        popup=f"{region_name}<br>Тип оборудования: {equipment_type}<br>Затраты: ${equipment_cost:.2f}<br>Доходы: ${revenue:.2f}",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("247.html")