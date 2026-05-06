python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import folium

# 1. Загрузка данных
data = pd.read_csv('real_estate.csv')

# 2. Обработка данных
# (Пример кода для обработки данных - нужно адаптировать под конкретные данные)
data = pd.get_dummies(data, columns=['district'])
X = data[['area', 'rooms', 'year', 'district_A', 'district_B', ...]]
y = data['price']

# 3. Разделение данных на обучающий и тестовый наборы
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 4. Обучение модели (Пример с Linear Regression)
model = LinearRegression()
model.fit(X_train, y_train)

# 5. Оценка модели
y_pred = model.predict(X_test)
print('R-squared:', r2_score(y_test, y_pred))
print('MAE:', mean_absolute_error(y_test, y_pred))
print('MSE:', mean_squared_error(y_test, y_pred))

# 6. Визуализация (Пример с folium)
m = folium.Map()
for index, row in data.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f'Price: {row["price"]}')\
        .add_to(m)

m.save('279.html')