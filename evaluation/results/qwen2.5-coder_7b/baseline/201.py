import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import folium
from folium.plugins import HeatMap

# Пример данных (замените на реальные данные)
data = {
    'date': pd.date_range(start='1/1/2020', periods=365),
    'temperature': np.random.randint(10, 40, size=365),
    'precipitation': np.random.rand(365) * 10,
    'river_level_Aksu': np.random.rand(365) * 100,
    'river_level_Lepsy': np.random.rand(365) * 100,
    'drought_risk': np.random.randint(0, 2, size=365)
}

df = pd.DataFrame(data)

# Преобразование даты в формат datetime
df['date'] = pd.to_datetime(df['date'])

# Разделение данных на признаки и целевую переменную
X = df[['temperature', 'precipitation', 'river_level_Aksu', 'river_level_Lepsy']]
y = df['drought_risk']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание модели случайного леса
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Прогнозирование на тестовой выборке
y_pred = model.predict(X_test)

# Оценка модели
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')
print(classification_report(y_test, y_pred))

# Визуализация риска засухи на карте
m = folium.Map(location=[40.7128, 74.0060], zoom_start=5)

# Добавление теплового карты для демонстрации плотности риска засухи
heat_data = [[row['latitude'], row['longitude'], row['drought_risk']] for index, row in df.iterrows()]
HeatMap(heat_data).add_to(m)

# Сохранение карты
m.save("201.html")