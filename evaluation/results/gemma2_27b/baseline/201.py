import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import folium

# Загрузить данные о засухе из CSV файла
data = pd.read_csv("drought_data.csv")

# Выбрать переменные для моделирования (например, осадки, температура)
features = ["precipitation", "temperature"]
target = "drought"

# Разделить данные на обучающий и тестовый набор
X_train, X_test, y_train, y_test = train_test_split(data[features], data[target], test_size=0.2)

# Обучить модель логистической регрессии
model = LogisticRegression()
model.fit(X_train, y_train)

# Прогнозировать риск засухи на тестовом наборе
predictions = model.predict(X_test)

# Создать карту с помощью folium
m = folium.Map(location=[41.58, 79.02], zoom_start=8)

# Добавить маркеры на карту (например, местоположение метеорологических станций)
for index, row in data.iterrows():
    folium.Marker(location=[row["latitude"], row["longitude"]]).add_to(m)

# Сохранить карту в HTML файл
m.save("201.html")