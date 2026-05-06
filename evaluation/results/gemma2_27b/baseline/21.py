import pandas as pd
from sklearn.linear_model import LinearRegression
import folium

# 1. Загрузка данных
data = pd.read_csv("shyzhyn_river_flow.csv")  # Заменить на имя файла с данными

# 2. Обработка данных (пример)
data['Season'] = pd.Categorical(data['Month'], categories=['Spring', 'Summer', 'Autumn', 'Winter'], ordered=True)
data = data.groupby(['Year', 'Season'])['Flow'].mean().reset_index()

# 3. Выбор модели (пример: линейная регрессия)
model = LinearRegression()

# 4. Обучение модели
X = pd.get_dummies(data['Season'], drop_first=True)
y = data['Flow']
model.fit(X, y)

# 5. Прогнозирование (пример: прогноз на следующий год)
future_seasons = pd.DataFrame({'Summer': [1], 'Autumn': [1], 'Winter': [1]})
predictions = model.predict(future_seasons)

# 6. Визуализация
m = folium.Map(location=[50.45, 30.52], zoom_start=10)  # Заменить на координаты реки Shyzhyn River

for i, season in enumerate(['Summer', 'Autumn', 'Winter']):
    folium.Marker(
        location=[50.45, 30.52],  # Заменить на координаты реки Shyzhyn River
        popup=f"{season}: {predictions[i]:.2f} m³/s",
        icon=folium.Icon(color='green', icon='info-sign')
    ).add_to(m)

m.save("21.html")