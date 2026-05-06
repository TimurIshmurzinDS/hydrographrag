import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import folium
from folium.plugins import MarkerCluster

# Пример данных: исторические данные о количестве осадков в регионе реки Турген
data = {
    'date': pd.date_range(start='1/1/2020', periods=365, freq='D'),
    'precipitation': np.random.normal(loc=50, scale=20, size=365)
}
df = pd.DataFrame(data)

# Анализ паттернов засухи
df['is_drought'] = df['precipitation'] < 10

# Создание модели ирригации (пример: количество полей и потребность в воде)
fields = {
    'field1': {'area': 10, 'water_consumption_per_day': 5},
    'field2': {'area': 15, 'water_consumption_per_day': 7}
}

# Оценка последствий засухи
def evaluate_drought_impact(df, fields):
    drought_days = df[df['is_drought']].shape[0]
    total_water_needed = sum(fields[field]['area'] * fields[field]['water_consumption_per_day'] for field in fields)
    
    if drought_days > 30:  # Если засуха длится более 30 дней
        impact = "Высокий риск"
    elif drought_days > 15:
        impact = "Средний риск"
    else:
        impact = "Низкий риск"
    
    return {
        'drought_days': drought_days,
        'total_water_needed': total_water_needed,
        'impact': impact
    }

drought_impact = evaluate_drought_impact(df, fields)
print(drought_impact)

# Визуализация на карте
m = folium.Map(location=[50.1234, 8.7654], zoom_start=10)

marker_cluster = MarkerCluster().add_to(m)

for index, row in df.iterrows():
    folium.Marker(
        location=[50.1234 + np.random.normal(scale=0.1), 8.7654 + np.random.normal(scale=0.1)],
        popup=f"Date: {row['date']}, Precipitation: {row['precipitation']} mm",
        icon=folium.Icon(color='red' if row['is_drought'] else 'green')
    ).add_to(marker_cluster)

m.save("189.html")