import pandas as pd
from sklearn.linear_model import LogisticRegression
import folium

# Шаг 1: Соберите данные о факторах для рек Шынжалгы и Шижын
shynzhaly_data = pd.read_csv('shynzhaly_data.csv')
shyzhyn_data = pd.read_csv('shyzhyn_data.csv')

# Шаг 2: Очистите и преобразуйте данные в формат, пригодный для моделирования риска наводнений
shynzhaly_data = shynzhaly_data.dropna()
shyzhyn_data = shyzhyn_data.dropna()

X_shynzhaly = shynzhaly_data[['river_height', 'flow_speed', 'rainfall_amount', 'catchment_area']]
y_shynzhaly = shynzhaly_data['flood_risk']

X_shyzhyn = shyzhyn_data[['river_height', 'flow_speed', 'rainfall_amount', 'catchment_area']]
y_shyzhyn = shyzhyn_data['flood_risk']

# Шаг 3: Создайте модель риска наводнений
model = LogisticRegression()
model.fit(X_shynzhaly, y_shynzhaly)

# Шаг 4: Введите данные о факторах для обеих рек в модель и получите оценку вероятности наводнений для каждой реки
shynzhaly_flood_risk = model.predict_proba(X_shynzhaly)[:, 1].mean()
shyzhyn_flood_risk = model.predict_proba(X_shyzhyn)[:, 1].mean()

# Шаг 5: Сравните полученные оценки и определите, какая река более подвержена наводнениям
if shynzhaly_flood_risk > shyzhyn_flood_risk:
    print("Шынжалгы река более подвержена наводнениям.")
else:
    print("Шижын река более подвержена наводнениям.")

# Визуализация данных на карте с использованием библиотеки folium
m = folium.Map(location=[43.2, 76.9], zoom_start=8)

folium.Marker([shynzhaly_data['latitude'].mean(), shynzhaly_data['longitude'].mean()],
              popup='Шынжалгы река\nВероятность наводнений: {:.2f}'.format(shynzhaly_flood_risk)).add_to(m)

folium.Marker([shyzhyn_data['latitude'].mean(), shyzhyn_data['longitude'].mean()],
              popup='Шижын река\nВероятность наводнений: {:.2f}'.format(shyzhyn_flood_risk)).add_to(m)

m.save("154.html")