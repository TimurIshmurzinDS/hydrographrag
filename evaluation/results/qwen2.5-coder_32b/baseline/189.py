import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import folium

# Шаг 1: Сбор данных (примерные данные)
data = {
    'date': pd.date_range(start='2015-01-01', periods=365*7, freq='D'),
    'flow_rate': np.random.normal(loc=100, scale=20, size=365*7),
    'temperature': np.random.uniform(low=-10, high=30, size=365*7),
    'precipitation': np.random.exponential(scale=1, size=365*7)
}

df = pd.DataFrame(data)

# Добавление признака засухи (пример: если поток воды ниже 80, считаем это засухой)
df['drought'] = df['flow_rate'].apply(lambda x: 1 if x < 80 else 0)

# Шаг 2: Предварительная обработка данных
df.dropna(inplace=True)

# Шаг 3: Анализ временных рядов (примерный анализ)
# Здесь можно использовать более сложные методы, но для простоты используем базовый подход

# Шаг 4: Моделирование вероятности засухи
X = df[['flow_rate', 'temperature', 'precipitation']]
y = df['drought']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Оценка модели
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Предсказание вероятности засухи на всех данных
df['drought_prob'] = model.predict_proba(df[['flow_rate', 'temperature', 'precipitation']])[:, 1]

# Шаг 5: Оценка последствий для ирригационных систем (простой пример)
# Предположим, что есть ирригационные системы в определенных точках
irrigation_systems = pd.DataFrame({
    'name': ['System1', 'System2'],
    'latitude': [43.05, 43.1],
    'longitude': [76.9, 77.0]
})

# Присвоение вероятности засухи каждой системе (пример)
irrigation_systems['drought_prob'] = df['drought_prob'].mean()

# Шаг 6: Визуализация результатов
m = folium.Map(location=[43.075, 76.95], zoom_start=10)

for _, row in irrigation_systems.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=row['drought_prob'] * 10,
        color='red' if row['drought_prob'] > 0.5 else 'green',
        fill=True,
        popup=f"System: {row['name']}<br>Drought Probability: {row['drought_prob']:.2f}"
    ).add_to(m)

m.save("189.html")