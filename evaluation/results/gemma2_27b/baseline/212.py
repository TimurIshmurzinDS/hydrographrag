import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import folium

# Загрузить данные о курсе биткоина и уровне воды
data = pd.read_csv("data.csv")

# Предобработать данные (удалить пропуски, преобразовать типы данных)

# Разделить данные на обучающий и тестовый наборы
X = data["Bitcoin Price"]
y = data["Water Level"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Обучить модель линейной регрессии
model = LinearRegression()
model.fit(X_train.values.reshape(-1, 1), y_train)

# Прогнозировать уровень воды на основе курса биткоина
predictions = model.predict(X_test.values.reshape(-1, 1))

# Оценить точность модели (R-squared, MAE, RMSE)

# Создать карту с помощью folium
m = folium.Map(location=[data["Latitude"].mean(), data["Longitude"].mean()], zoom_start=10)
folium.Marker([data["Latitude"].mean(), data["Longitude"].mean()], popup="Batareyka River").add_to(m)

# Сохранить карту
m.save("212.html")