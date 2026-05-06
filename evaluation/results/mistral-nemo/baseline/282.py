import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import folium

# Шаг 1: Сбор данных
data = pd.read_csv('crypto_data.csv')

# Шаг 2: Подготовка данных
data.drop_duplicates(inplace=True)
data.fillna(method='ffill', inplace=True)
data['price'] = (data['price'] - data['price'].mean()) / data['price'].std()
data['volatility'] = (data['volatility'] - data['volatility'].mean()) / data['volatility'].std()

# Шаг 3: Выбор признаков
X = data[['volatility']]
y = data['price']

# Шаг 4: Разделение данных
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Шаг 5: Обучение модели
model = LinearRegression()
model.fit(X_train, y_train)

# Шаг 6: Оценка модели
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f'MAE: {mae}')

# Шаг 7: Визуализация результатов на карте
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=2)

for i in range(len(data)):
    folium.CircleMarker(
        location=[data.iloc[i]['latitude'], data.iloc[i]['longitude']],
        radius=data.iloc[i]['price'],
        color='blue',
        fill=True,
        fill_opacity=0.5
    ).add_to(m)

m.save("282.html")