import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
import folium

# Предположим, что у нас есть исторические данные в CSV формате
data = pd.read_csv('historical_data.csv')

# Пример данных (замените на реальные данные)
# data = pd.DataFrame({
#     'date': pd.date_range(start='2010-01-01', periods=365*10, freq='D'),
#     'temperature': np.random.uniform(10, 40, size=365*10),
#     'precipitation': np.random.uniform(0, 20, size=365*10),
#     'water_level_aksu': np.random.uniform(800, 1200, size=365*10),
#     'water_level_lepsy': np.random.uniform(700, 1100, size=365*10),
#     'drought_risk': np.random.choice([0, 1], size=365*10)  # 0 - нет риска, 1 - есть риск
# })

# Предобработка данных
data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)
data.fillna(method='ffill', inplace=True)

# Выбор признаков и целевой переменной
features = ['temperature', 'precipitation', 'water_level_aksu', 'water_level_lepsy']
X = data[features]
y = data['drought_risk']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Построение модели случайного леса
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Прогнозирование на тестовой выборке
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

# Оценка модели
print(classification_report(y_test, y_pred))
print('ROC-AUC:', roc_auc_score(y_test, y_proba))

# Прогнозирование риска засухи на всей выборке
data['drought_risk_pred'] = model.predict(X)
data['drought_risk_proba'] = model.predict_proba(X)[:, 1]

# Визуализация результатов на карте с использованием folium
# Предположим, что у нас есть координаты точек измерений (замените на реальные данные)
coordinates = pd.DataFrame({
    'latitude': np.random.uniform(40.5, 41.5, size=len(data)),
    'longitude': np.random.uniform(76.5, 78.5, size=len(data))
})

# Создание карты
m = folium.Map(location=[41.0, 77.5], zoom_start=9)

# Добавление маркеров на карту с цветом в зависимости от риска засухи
for i in range(len(coordinates)):
    if data['drought_risk_pred'].iloc[i] == 1:
        color = 'red'
    else:
        color = 'green'
    folium.CircleMarker(
        location=[coordinates['latitude'].iloc[i], coordinates['longitude'].iloc[i]],
        radius=5,
        color=color,
        fill=True,
        fill_color=color
    ).add_to(m)

# Сохранение карты в HTML файл
m.save("201.html")