import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from folium import Map, Marker

# Сбор и очистка данных
data = {
    'Дата': ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01', '2022-05-01'],
    'Река': ['Tekeli River', 'Tekeli River', 'Lepsy River', 'Lepsy River', 'Tekeli River'],
    'Уровень воды (м)': [10, 12, 15, 18, 20]
}
df = pd.DataFrame(data)

# Анализ данных
print(df.groupby('Река')['Уровень воды (м)'].mean())

# Создание модели прогнозирования уровня воды
X = df[['Дата']]
y = df['Уровень воды (м)']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)

# Оценка стабильности уровня воды
predictions = model.predict(X_test)
print(predictions)

# Визуализация результатов на карте
m = Map(location=[50.1234, 36.4567], zoom_start=10)
for index, row in df.iterrows():
    Marker(row['Дата'], row['Река'], icon=None).add_to(m)
m.save("116.html")