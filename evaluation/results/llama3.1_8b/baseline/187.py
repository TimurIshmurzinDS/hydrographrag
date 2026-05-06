import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import folium

# Подготовка данных
data = {
    'Хозяйство': ['Хозяйство 1', 'Хозяйство 2', 'Хозяйство 3'],
    'Уровень реки (м)': [10, 15, 20],
    'Потребление воды (тыс. м³)': [1000, 1500, 2000]
}

df = pd.DataFrame(data)

# Разделение данных на обучающую и тестовую выборки
X = df[['Уровень реки (м)']]
y = df['Потребление воды (тыс. м³)']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание и обучение модели
model = LinearRegression()
model.fit(X_train, y_train)

# Прогнозирование потребления воды для снижения уровня реки на 5 м
new_data = pd.DataFrame({'Уровень реки (м)': [5]})
predicted_water_consumption = model.predict(new_data)
print(f'Предсказанная потребность в воде при снижении уровня реки на 5 м: {predicted_water_consumption[0]} тыс. м³')

# Визуализация результатов на карте
m = folium.Map(location=[55.76, 82.96], zoom_start=10)
folium.Marker([55.76, 82.96], popup=f'Предсказанная потребность в воде: {predicted_water_consumption[0]} тыс. м³').add_to(m)
m.save("187.html")