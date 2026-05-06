import pandas as pd
import folium

# Шаг 1: Сбор данных
data = pd.read_csv('historical_housing_costs.csv')

# Шаг 2: Очистка данных
data = data.dropna()

# Шаг 3: Агрегация данных
aggregated_data = data.groupby(['city', 'year'])['cost'].mean().reset_index()

# Шаг 4: Создание модели (в данном примере используется простая линейная регрессия)
from sklearn.linear_model import LinearRegression

X = pd.get_dummies(aggregated_data[['city']], columns=['city'])
y = aggregated_data['cost']
model = LinearRegression()
model.fit(X, y)

# Шаг 5: Визуализация результатов
m = folium.Map(location=[40.7128, -74.0060], zoom_start=3) # Нью-Йорк как центр карты

for index, row in aggregated_data.iterrows():
    city = row['city']
    year = row['year']
    cost = model.predict(X.loc[X[city] == 1])[-1]
    folium.CircleMarker(location=[row['lat'], row['lon']], radius=5, fill=True,
                        color='blue', fill_opacity=0.7).add_to(m)
    folium.Marker([row['lat'], row['lon']], popup=f'{city} ({year}): ${cost:.2f}').add_to(m)

# Шаг 6: Сохранение результатов
m.save("280.html")