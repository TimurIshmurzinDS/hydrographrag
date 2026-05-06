import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from folium import Map, Marker

# Загрузка данных о расходе воды на реках Баскан и Прохождение
data_baskan = pd.read_csv('baskan_data.csv')
data_prokhodnaya = pd.read_csv('prokhodnaya_data.csv')

# Объединение данных в одну таблицу
data = pd.concat([data_baskan, data_prokhodnaya])

# Создание модели регрессии для предсказания уровня воды в реке
X = data[['season', 'temperature', 'precipitation']]
y = data['water_level']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

# Создание интерактивной карты с результатами моделирования
m = Map(location=[55.76, 37.62], zoom_start=10)
marker_baskan = Marker(location=[55.76, 37.62], popup='Река Баскан')
marker_prokhodnaya = Marker(location=[56.12, 38.15], popup='Река Прохождение')

m.add_child(marker_baskan)
m.add_child(marker_prokhodnaya)

# Добавление результатов моделирования на карту
for i in range(len(data)):
    predicted_water_level = model.predict([[data['season'][i], data['temperature'][i], data['precipitation'][i]]])
    marker = Marker(location=[data['latitude'][i], data['longitude'][i]], popup=f'Прогноз уровня воды: {predicted_water_level[0]}')
    m.add_child(marker)

# Сохранение карты в файл
m.save('77.html')