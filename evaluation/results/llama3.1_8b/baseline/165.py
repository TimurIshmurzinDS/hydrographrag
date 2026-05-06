import pandas as pd
from folium import Map, Marker, CircleMarker
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Сбор данных о уровнях воды в реках Shyzhyn River и Sarykan River за последние 10 лет.
data = {
    'Date': ['2020-01-01', '2020-02-01', '2020-03-01', '2020-04-01', '2020-05-01',
             '2020-06-01', '2020-07-01', '2020-08-01', '2020-09-01', '2020-10-01'],
    'Shyzhyn River': [5.2, 4.8, 6.1, 7.3, 8.5, 9.2, 10.1, 11.3, 12.5, 13.2],
    'Sarykan River': [3.5, 4.1, 5.3, 6.5, 7.7, 8.4, 9.3, 10.5, 11.7, 12.4]
}

df = pd.DataFrame(data)

# Анализ данных для выявления закономерностей и тенденций в изменении уровней воды.
plt.figure(figsize=(10,6))
plt.plot(df['Date'], df['Shyzhyn River'], label='Shyzhyn River')
plt.plot(df['Date'], df['Sarykan River'], label='Sarykan River')
plt.xlabel('Дата')
plt.ylabel('Уровень воды (м)')
plt.title('Анализ уровней воды в реках Shyzhyn River и Sarykan River')
plt.legend()
plt.show()

# Создание модели прогнозирования паводков на основе анализа данных.
X = df[['Shyzhyn River', 'Sarykan River']]
y = df['Date']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print('Коэффициент детерминации:', model.score(X_test, y_test))
print('Среднеквадратическая ошибка:', mean_squared_error(y_test, y_pred))

# Визуализация результатов анализа и прогноза на карте с помощью библиотеки Folium.
m = Map(location=[50.0, 70.0], zoom_start=6)

marker1 = Marker(location=[50.0, 70.0], popup='Река Shyzhyn River')
marker2 = Marker(location=[55.0, 75.0], popup='Река Sarykan River')

circle1 = CircleMarker(location=[50.0, 70.0], radius=10000, color='red', fill=True)
circle2 = CircleMarker(location=[55.0, 75.0], radius=15000, color='blue', fill=True)

m.add_child(marker1)
m.add_child(marker2)
m.add_child(circle1)
m.add_child(circle2)

m.save("165.html")