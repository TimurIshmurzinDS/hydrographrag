import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import folium
from folium.plugins import HeatMap

# 1. Генерация синтетических исторических данных для бассейнов рек Aksu и Kishi Osek
# В реальном сценарии здесь будет загрузка CSV или API данных (например, ERA5 или гидропосты)
np.random.seed(42)

def generate_river_data(river_name, coords, n_points=50):
    data = []
    for i in range(n_points):
        lat = coords[0] + np.random.uniform(-0.2, 0.2)
        lon = coords[1] + np.random.uniform(-0.2, 0.2)
        # Исторические показатели за 10 лет (120 месяцев)
        for month in range(120):
            precip = np.random.gamma(2, 2) + np.sin(month * np.pi / 6) * 2 # Сезонность
            temp = 15 + 10 * np.sin(month * np.pi / 6) + np.random.normal(0, 2)
            # Доступность воды зависит от осадков и температуры (испарение)
            water_avail = (precip * 0.7) - (temp * 0.1) + np.random.normal(0, 1)
            data.append([river_name, lat, lon, month, precip, temp, water_avail])
    return data

# Координаты (приблизительные для региона Центральной Азии)
aksu_coords = [42.5, 77.5]
kishi_osek_coords = [42.8, 77.2]

all_data = generate_river_data("Aksu", aksu_coords) + generate_river_data("Kishi Osek", kishi_osek_coords)
df = pd.DataFrame(all_data, columns=['River', 'Lat', 'Lon', 'Month', 'Precipitation', 'Temperature', 'Water_Availability'])

# 2. Построение прогностической модели
# Подготовка признаков (X) и целевой переменной (y)
X = df[['Precipitation', 'Temperature']]
y = df['Water_Availability']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Проверка точности
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f"Model Mean Absolute Error: {mae:.4f}")

# 3. Прогноз доступности воды на будущий период для каждой точки
# Создаем "будущие" климатические условия (средние значения + шум)
future_precip = np.random.normal(4.0, 1.0, len(df['Lat'].unique())) 
future_temp = np.random.normal(15.0, 3.0, len(df['Lat'].unique()))

# Получаем уникальные точки бассейнов
unique_points = df[['Lat', 'Lon', 'River']].drop_duplicates().reset_index(drop=True)
future_features = pd.DataFrame({
    'Precipitation': np.random.normal(5, 2, len(unique_points)),
    'Temperature': np.random.normal(18, 5, len(unique_points))
})

unique_points['Predicted_Availability'] = model.predict(future_features)

# 4. Визуализация на карте
# Центр карты
m = folium.Map(location=[42.6, 77.3], zoom_start=8, tiles='CartoDB positron')

# Добавление точек с цветовой индикацией
for idx, row in unique_points.iterrows():
    # Определяем цвет в зависимости от доступности воды
    if row['Predicted_Availability'] > 2:
        color = 'blue'   # Высокая доступность
    elif row['Predicted_Availability'] > 0:
        color = 'green'  # Средняя доступность
    else:
        color = 'red'    # Низкая доступность/Дефицит

    folium.CircleMarker(
        location=[row['Lat'], row['Lon']],
        radius=6,
        popup=f"River: {row['River']}<br>Pred. Availability: {row['Predicted_Availability']:.2f}",
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(m)

# Добавление тепловой карты для общего понимания зон риска
heat_data = [[row['Lat'], row['Lon'], row['Predicted_Availability']] for idx, row in unique_points.iterrows()]
HeatMap(heat_data, radius=15, blur=20, min_opacity=0.5).add_to(m)

# Сохранение карты
m.save("206.html")
print("Map has been saved as 206.html")