import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import folium
from folium.plugins import HeatMap

# 1. Симуляция данных (так как реальные исторические данные требуют доступа к API/БД)
# Создаем синтетический набор данных для бассейна рек Аксу и Лепсы
def generate_basin_data(n_points=500):
    np.random.seed(42)
    # Координаты примерно в районе бассейна рек Аксу и Лепсы (Казахстан/Китай)
    lat_min, lat_max = 43.0, 45.0
    lon_min, lon_max = 78.0, 82.0
    
    data = {
        'lat': np.random.uniform(lat_min, lat_max, n_points),
        'lon': np.random.uniform(lon_min, lon_max, n_points),
        'precip_hist': np.random.uniform(100, 500, n_points), # Осадки в мм
        'temp_hist': np.random.uniform(15, 30, n_points),    # Средняя летняя темп.
        'ndvi_hist': np.random.uniform(0.2, 0.7, n_points),   # Индекс растительности
        'elevation': np.random.uniform(200, 1500, n_points)   # Высота над уровнем моря
    }
    
    df = pd.DataFrame(data)
    
    # Создаем целевую переменную 'drought_risk' на основе логики: 
    # Низкие осадки + Высокая температура + Низкий NDVI = Высокий риск
    df['drought_risk'] = (
        (500 - df['precip_hist']) * 0.5 + 
        (df['temp_hist'] * 2) - 
        (df['ndvi_hist'] * 100) + 
        np.random.normal(0, 10, n_points)
    )
    # Нормализуем риск от 0 до 1
    df['drought_risk'] = (df['drought_risk'] - df['drought_risk'].min()) / \
                         (df['drought_risk'].max() - df['drought_risk'].min())
    return df

# 2. Подготовка модели
df = generate_basin_data()

# Признаки и целевая переменная
X = df[['precip_hist', 'temp_hist', 'ndvi_hist', 'elevation']]
y = df['drought_risk']

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Масштабирование данных
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Обучение модели Random Forest
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Прогноз рисков для всех точек бассейна
df['predicted_risk'] = model.predict(scaler.transform(X))

# 3. Визуализация с помощью Folium
# Создаем карту, центрированную в регионе
m = folium.Map(location=[44.0, 80.0], zoom_start=7, tiles='CartoDB positron')

# Функция для определения цвета в зависимости от риска
def get_color(risk):
    if risk > 0.7:
        return 'red'    # Высокий риск
    elif risk > 0.4:
        return 'orange' # Средний риск
    else:
        return 'green'  # Низкий риск

# Добавление точек риска на карту
for idx, row in df.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=5,
        color=get_color(row['predicted_risk']),
        fill=True,
        fill_color=get_color(row['predicted_risk']),
        fill_opacity=0.7,
        popup=f"Risk: {row['predicted_risk']:.2f}"
    ).add_to(m)

# Добавление легенды (простой текстовый элемент)
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 150px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Риск засухи:</b><br>
     <i style="background:red;width:10px;height:10px;display:inline-block"></i> Высокий<br>
     <i style="background:orange;width:10px;height:10px;display:inline-block"></i> Средний<br>
     <i style="background:green;width:10px;height:10px;display:inline-block"></i> Низкий
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение карты
m.save("201.html")

print("Модель успешно построена. Карта рисков сохранена в файл 201.html")