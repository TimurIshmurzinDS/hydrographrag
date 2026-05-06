# Импорт необходимых библиотек
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import folium

# Загрузка данных о ценах на нефть и популяции рыб в реке Бутак
data = {
    'цена_нефти': [50, 60, 70, 80, 90],
    'популяция_рыб': [1000, 1200, 1500, 1800, 2000]
}
df = pd.DataFrame(data)

# Разделение данных на обучающую и тестовую выборки
X = df[['цена_нефти']]
y = df['популяция_рыб']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Обучение модели регрессии
model = LinearRegression()
model.fit(X_train, y_train)

# Предсказание популяции рыб в реке Бутак на основе текущих цен на нефть
current_price = 85
predicted_population = model.predict([[current_price]])

# Оценка качества модели
mse = mean_squared_error(y_test, model.predict(X_test))

# Создание карты с предсказанной популяцией рыб в реке Бутак
m = folium.Map(location=[45.0, 80.0], zoom_start=10)
folium.Marker([45.0, 80.0], popup=f'Предсказанная популяция рыб: {predicted_population[0]}').add_to(m)

# Сохранение карты в файл
m.save("262.html")