import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import folium

# 1. Симуляция исторических данных солнечных циклов
# В реальном сценарии здесь будет загрузка CSV из NOAA
def generate_solar_data(days=3650):
    np.random.seed(42)
    time = np.arange(days)
    
    # Симуляция 11-летнего цикла (синусоида + шум)
    sunspot_number = 100 * (np.sin(2 * np.pi * time / (11 * 365)) + 1) + np.random.normal(0, 20, days)
    x_ray_flux = np.exp(np.random.normal(loc=np.log(sunspot_number/100 + 1), scale=0.5, size=days))
    
    # Целевая переменная: вспышка происходит, если активность выше порога + случайный фактор
    flare_occurred = ((sunspot_number > 150) & (np.random.rand(days) > 0.7)).astype(int)
    
    df = pd.DataFrame({
        'day': time,
        'ssn': sunspot_number,
        'x_ray': x_ray_flux,
        'flare': flare_occurred
    })
    return df

# 2. Предобработка и Feature Engineering
def prepare_features(df):
    # Создаем лаги (предыдущие значения)
    for lag in [1, 3, 7]:
        df[f'ssn_lag_{lag}'] = df['ssn'].shift(lag)
        df[f'x_ray_lag_{lag}'] = df['x_ray'].shift(lag)
    
    # Скользящее среднее
    df['ssn_rolling_7'] = df['ssn'].rolling(window=7).mean()
    
    df = df.dropna()
    return df

# --- Основной процесс ---

# Генерация и подготовка данных
data = generate_solar_data()
data_featured = prepare_features(data)

X = data_featured.drop(['day', 'flare'], axis=1)
y = data_featured['flare']

# Разделение на обучающую и тестовую выборки (по времени)
split = int(len(X) * 0.8)
X_train, X_test = X.iloc[:split], X.iloc[split:]
y_train, y_test = y.iloc[:split], y.iloc[split:]

# Обучение модели
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Предсказание вероятности для последнего доступного состояния
last_state = X.tail(1)
prob = model.predict_proba(last_state)[0][1]
print(f"Predicted probability of a solar flare: {prob:.2%}")

# 3. Геопространственная визуализация влияния
# Солнечные вспышки влияют на магнитосферу, особенно в полярных регионах.
# Создадим карту с зонами риска (Auroral Oval)

m = folium.Map(location=[0, 0], zoom_start=2, tiles='CartoDB dark_matter')

# Определяем зоны риска (высокие широты)
# Если вероятность высокая, рисуем более широкие зоны
risk_radius = 500000 * (1 + prob * 10) # Радиус зависит от вероятности

# Координаты магнитных полюсов (приблизительно)
poles = [
    {"name": "North Magnetic Pole", "coords": [86.5, 164.0]},
    {"name": "South Magnetic Pole", "coords": [-64.0, -136.0]}
]

for pole in poles:
    folium.Circle(
        location=pole["coords"],
        radius=risk_radius,
        color='yellow',
        fill=True,
        fill_color='orange',
        fill_opacity=0.4,
        popup=f"Risk Zone: {pole['name']} (Prob: {prob:.2%})"
    ).add_to(m)

# Добавляем текстовую метку с вероятностью
folium.Marker(
    location=[0, 0],
    icon=folium.DivIcon(html=f"""<div style="font-size: 20pt; color: white; font-weight: bold;">
                                    Solar Flare Probability: {prob:.2%}</div>""")
).add_to(m)

# Сохранение карты
m.save("275.html")
print("Map saved as 275.html")