import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import folium

# 1. Подготовьте данные
data = pd.read_csv('bayankol_data.csv')

# 2. Очистите данные
data.dropna(inplace=True)

# 3. Преобразование данных
scaler = MinMaxScaler()
data['water_level_norm'] = scaler.fit_transform(data[['water_level']])

# 4. Разделение данных
X = data[['water_level_norm']]
y = data['token_price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Обучение модели
model = LinearRegression()
model.fit(X_train, y_train)

# 6. Прогнозирование
predictions = model.predict(X_test)

# 7. Визуализация
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

for i in range(len(data)):
    folium.CircleMarker(
        location=[data.iloc[i]['latitude'], data.iloc[i]['longitude']],
        radius=predictions[i]*5,  # Увеличьте радиус для лучшей видимости
        color='blue',
        fill=True,
        fill_opacity=0.3
    ).add_to(m)

m.save("264.html")