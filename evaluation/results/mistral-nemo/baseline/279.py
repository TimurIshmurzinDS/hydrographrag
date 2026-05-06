import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import folium

# 1. Подготовка данных
data = pd.read_csv('housing.csv')

# 2. Преобразование географических координат
data['longitude'] = data['longitude'].apply(lambda x: x * 0.00001)
data['latitude'] = data['latitude'].apply(lambda x: x * 0.00001)

# 3. Подготовка признаков
X = data[['longitude', 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income']]
y = data['median_house_value']

# 4. Разделение данных
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Регрессионный анализ
model = LinearRegression()
model.fit(X_train, y_train)

# 6. Оценка модели
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'MAE: {mae}')
print(f'R^2: {r2}')

# 7. Визуализация результатов
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

for i in range(len(data)):
    folium.CircleMarker(
        location=[data.iloc[i]['latitude'], data.iloc[i]['longitude']],
        radius=5,
        color='blue',
        fill=True,
        fill_opacity=0.5
    ).add_to(m)

m.save("279.html")